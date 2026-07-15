import datetime
from app.models.trek import Trek
from app.models.booking import Booking

def get_monthly_report_data():
    today = datetime.date.today()
    first_day_this_month = today.replace(day=1)
    last_day_last_month = first_day_this_month - datetime.timedelta(days=1)
    first_day_last_month = last_day_last_month.replace(day=1)

    treks_conducted = Trek.query.filter(Trek.start_date >= first_day_last_month, Trek.start_date <= last_day_last_month).all()
    
    total_conducted = len(treks_conducted)
    total_participants = 0
    trek_participant_counts = {}
    
    for t in treks_conducted:
        bookings = Booking.query.filter_by(trek_id=t.id).filter(Booking.status.in_([Booking.STATUS_BOOKED, Booking.STATUS_COMPLETED])).all()
        slots_sum = sum(b.slots_booked for b in bookings)
        total_participants += slots_sum
        trek_participant_counts[t.name] = trek_participant_counts.get(t.name, 0) + slots_sum
        
    popular_trek_name = "N/A"
    popular_trek_count = 0
    if trek_participant_counts:
        popular_trek_name = max(trek_participant_counts, key=trek_participant_counts.get)
        popular_trek_count = trek_participant_counts[popular_trek_name]
        

    bookings_last_month = Booking.query.filter(Booking.booking_date >= datetime.datetime.combine(first_day_last_month, datetime.time.min), 
        Booking.booking_date <= datetime.datetime.combine(last_day_last_month, datetime.time.max)).all()
    
    total_bookings = len(bookings_last_month)
    booked_count = sum(1 for b in bookings_last_month if b.status == Booking.STATUS_BOOKED)
    completed_count = sum(1 for b in bookings_last_month if b.status == Booking.STATUS_COMPLETED)
    cancelled_count = sum(1 for b in bookings_last_month if b.status == Booking.STATUS_CANCELLED)
    
    return {
        "month_name": first_day_last_month.strftime("%B %Y"),
        "total_conducted": total_conducted,
        "total_participants": total_participants,
        "popular_trek_name": popular_trek_name,
        "popular_trek_count": popular_trek_count,
        "total_bookings": total_bookings,
        "booked_count": booked_count,
        "completed_count": completed_count,
        "cancelled_count": cancelled_count,
        "treks": [
            {
                "id": t.id,
                "name": t.name,
                "location": t.location,
                "status": t.status,
                "participants": trek_participant_counts.get(t.name, 0),
                "max_slots": t.max_slots
            } for t in treks_conducted
        ]
    }
