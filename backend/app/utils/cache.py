import functools
import hashlib
import json
from flask import request, g, make_response, jsonify
from app.extensions import cache_db

def cached(timeout=300, key_prefix="cache", query_params=True, user_specific=False):
    """Flask Redis caching decorator. Generates deterministic cache keys and falls back gracefully if Redis is offline.
    Adds X-Cache: HIT/MISS response headers."""

    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):

            ## generate cache key segments
            parts = [key_prefix, f.__name__]
            
            ## user specific scoping
            if user_specific:
                if hasattr(g, "current_user") and g.current_user:
                    parts.append(f"user_{g.current_user.id}")
                else:
                    parts.append("anon")
                    
            ## keyword arguments (ex: trek_id)
            if kwargs:
                sorted_kwargs = sorted(kwargs.items())
                parts.append(f"kwargs_{'_'.join(f'{k}:{v}' for k, v in sorted_kwargs)}")
                
                
            if query_params and request.args:
                sorted_args = sorted(request.args.items())
                arg_str = '&'.join(f"{k}={v}" for k, v in sorted_args)
                arg_hash = hashlib.md5(arg_str.encode('utf-8')).hexdigest()
                parts.append(f"args_{arg_hash}")
                
            cache_key = ":".join(parts)
            

            try:
                cached_data = cache_db.get(cache_key)
                if cached_data:
                    data, status_code, headers = json.loads(cached_data)
                    response = make_response(jsonify(data) if isinstance(data, (dict, list)) else data, status_code)
                    for k, v in headers.items():
                        response.headers[k] = v
                    response.headers["X-Cache"] = "HIT"
                    return response
            except Exception as e:
                print(f"Redis Cache connection error during get for key {cache_key}: {e}")
                
            
            response_value = f(*args, **kwargs)
            status_code = 200
            headers = {"Content-Type": "application/json"}
            data = response_value
            
            if isinstance(response_value, tuple):
                if len(response_value) >= 1:
                    data = response_value[0]
                if len(response_value) >= 2:
                    status_code = response_value[1]
                if len(response_value) >= 3:
                    headers = response_value[2]
            elif hasattr(response_value, "get_json"):
                data = response_value.get_json()
                status_code = response_value.status_code
                headers = dict(response_value.headers)
                
            try:
                if 200 <= status_code < 300:
                    serialized = json.dumps((data, status_code, headers))
                    cache_db.setex(cache_key, timeout, serialized)
            except Exception as e:
                print(f"Redis Cache connection error during set for key {cache_key}: {e}")
                

            res = make_response(response_value)
            res.headers["X-Cache"] = "MISS"
            return res
            
        return decorated_function
    return decorator


def cache_invalidate(pattern):
    """Deletes keys matching the pattern from Redis."""
    try:
        keys = cache_db.keys(pattern)
        if keys:
            cache_db.delete(*keys)
            print(f"Cache invalidated successfully for pattern: {pattern}")
    except Exception as e:
        print(f"Redis Cache invalidation error for pattern {pattern}: {e}")


def invalidate_trek_cache(trek_id=None):
    """Invalidates all public trek listings, public stats, admin summary, and the specific trek detail cache if trek_id is provided."""
    cache_invalidate("public_treks:*")
    cache_invalidate("public_stats:*")
    cache_invalidate("admin_summary:*")
    if trek_id:
        cache_invalidate(f"public_trek_detail:*:kwargs_trek_id:{trek_id}*")


def invalidate_booking_cache(user_id=None, guide_id=None):
    """Invalidates caching on user bookings dashboard, staff dashboard, public stats, public treks (for slots updates), and admin dashboard."""
    cache_invalidate("public_stats:*")
    cache_invalidate("public_treks:*")
    cache_invalidate("admin_summary:*")
    if user_id:
        cache_invalidate(f"user_dashboard:*:user_{user_id}*")
    if guide_id:
        cache_invalidate(f"staff_dashboard:*:user_{guide_id}*")
