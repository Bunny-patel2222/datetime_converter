from flask import Flask, render_template, request, jsonify
import pytz
from datetime import datetime

app = Flask(__name__)

# ─── Pre-compute timezone list at startup ───────────────────────────────────
def build_timezone_list():
    """Build a sorted list of all timezones with UTC offset labels."""
    result = []
    # Use a fixed reference time to avoid DST variance per request
    ref = datetime(2026, 1, 15, 12, 0, 0)  # mid-winter reference
    for tz_name in pytz.all_timezones:
        try:
            tz = pytz.timezone(tz_name)
            aware = tz.localize(ref)
            offset = aware.utcoffset()
            total_seconds = int(offset.total_seconds())
            sign = '+' if total_seconds >= 0 else '-'
            abs_secs = abs(total_seconds)
            hours, rem = divmod(abs_secs, 3600)
            minutes = rem // 60
            offset_str = f"UTC{sign}{hours:02d}:{minutes:02d}"

            parts = tz_name.split('/')
            if len(parts) >= 2:
                city = parts[-1].replace('_', ' ')
                region = parts[-2].replace('_', ' ') if len(parts) >= 3 else parts[0]
                label = f"{city}, {region} ({offset_str})"
            else:
                label = f"{tz_name} ({offset_str})"

            result.append({
                'id': tz_name,
                'label': label,
                '_offset_secs': total_seconds,
            })
        except Exception:
            pass

    result.sort(key=lambda x: (x['_offset_secs'], x['label']))
    # Remove internal sort key before returning
    for item in result:
        del item['_offset_secs']
    return result


# Cache at module load time
TIMEZONE_LIST = build_timezone_list()

# Lookup: tz_name -> UTC offset string (for convert endpoint)
_TZ_OFFSET_CACHE = {}
def get_utc_offset(tz_name):
    if tz_name in _TZ_OFFSET_CACHE:
        return _TZ_OFFSET_CACHE[tz_name]
    try:
        tz = pytz.timezone(tz_name)
        now = datetime.now(tz)
        offset = now.utcoffset()
        total_seconds = int(offset.total_seconds())
        sign = '+' if total_seconds >= 0 else '-'
        total_seconds = abs(total_seconds)
        hours, rem = divmod(total_seconds, 3600)
        minutes = rem // 60
        result = f"UTC{sign}{hours:02d}:{minutes:02d}"
    except Exception:
        result = "UTC+00:00"
    _TZ_OFFSET_CACHE[tz_name] = result
    return result


def format_tz_label(tz_name):
    offset_str = get_utc_offset(tz_name)
    parts = tz_name.split('/')
    if len(parts) >= 2:
        city = parts[-1].replace('_', ' ')
        region = parts[-2].replace('_', ' ') if len(parts) >= 3 else parts[0]
        return f"{city}, {region} ({offset_str})"
    return f"{tz_name} ({offset_str})"


# ─── Routes ────────────────────────────────────────────────────────────────
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/timezones')
def get_timezones():
    """Return pre-computed timezone list (instant response)."""
    return jsonify(TIMEZONE_LIST)


@app.route('/api/convert', methods=['POST'])
def convert_time():
    data = request.get_json()
    dt_str     = data.get('datetime')
    from_tz_str = data.get('from_tz')
    to_tz_str   = data.get('to_tz')

    if not dt_str or not from_tz_str or not to_tz_str:
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        from_tz = pytz.timezone(from_tz_str)
        to_tz   = pytz.timezone(to_tz_str)

        naive_dt   = datetime.strptime(dt_str, '%Y-%m-%dT%H:%M')
        aware_dt   = from_tz.localize(naive_dt)
        converted  = aware_dt.astimezone(to_tz)

        return jsonify({
            'converted_datetime':    converted.strftime('%A, %B %d, %Y  %I:%M %p'),
            'converted_datetime_24h': converted.strftime('%Y-%m-%d %H:%M:%S'),
            'timezone_name':         to_tz_str,
            'timezone_label':        format_tz_label(to_tz_str),
            'utc_offset':            get_utc_offset(to_tz_str),
            'original_datetime':     aware_dt.strftime('%A, %B %d, %Y  %I:%M %p'),
            'original_timezone_label': format_tz_label(from_tz_str),
        })
    except pytz.UnknownTimeZoneError as e:
        return jsonify({'error': f'Unknown timezone: {e}'}), 400
    except ValueError as e:
        return jsonify({'error': f'Invalid datetime format: {e}'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    print("Pre-loading timezone cache complete. Starting server...")
    app.run(debug=False, port=5000)
