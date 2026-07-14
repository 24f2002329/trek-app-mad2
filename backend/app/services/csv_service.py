import csv
import io

def generate_bookings_csv(bookings):
    """
    Generates CSV content for a list of booking models.
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow([
        "Booking ID", 
        "Trek Name", 
        "Location", 
        "Start Date", 
        "End Date", 
        "Slots Booked", 
        "Booking Date", 
        "Status"
    ])
    
    # Write rows
    for b in bookings:
        writer.writerow([
            b.id,
            b.trek.name if b.trek else "N/A",
            b.trek.location if b.trek else "N/A",
            b.trek.start_date.isoformat() if b.trek and b.trek.start_date else "N/A",
            b.trek.end_date.isoformat() if b.trek and b.trek.end_date else "N/A",
            b.slots_booked,
            b.booking_date.isoformat() if b.booking_date else "N/A",
            b.status
        ])
        
    return output.getvalue()
