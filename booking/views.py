from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Room, Booking, ClassSchedule
from .forms import BookingForm
from django.contrib import messages

def home(request):
    return render(request, 'booking/home.html')

def room_list(request):
    # Fetch all rooms from the database
    rooms = Room.objects.all() 
    # Send them to the template
    return render(request, 'booking/room_list.html', {'rooms': rooms})

@login_required
def book_room(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Get the data from the form without saving yet
            new_booking = form.save(commit=False)
            room = new_booking.room
            date = new_booking.date
            start_time = new_booking.start_time
            end_time = new_booking.end_time

            # --- 1. CHECK EXISTING BOOKINGS ---
            existing_bookings = Booking.objects.filter(
                room=room, 
                date=date, 
                status__in=['PENDING', 'APPROVED']
            )

            has_conflict = False
            conflict_reason = ""

            for booking in existing_bookings:
                if (start_time < booking.end_time) and (end_time > booking.start_time):
                    has_conflict = True
                    conflict_reason = f"another user's booking ({booking.reference_no})"
                    break

            # --- 2. CHECK CLASS SCHEDULES ---
            if not has_conflict:
                # Convert the date to a 3-letter day code (e.g., 'MON', 'TUE')
                day_requested = date.strftime('%a').upper()[:3]
                
                # Fetch class schedules for this room on this specific day
                class_schedules = ClassSchedule.objects.filter(
                    room=room,
                    day_of_week=day_requested
                )

                for sched in class_schedules:
                    if (start_time < sched.end_time) and (end_time > sched.start_time):
                        has_conflict = True
                        conflict_reason = f"a regular class ({sched.subject_name})"
                        break

            # --- 3. HANDLE THE CONFLICT ---
            if has_conflict:
                messages.error(request, f"Conflict! This room is reserved for {conflict_reason} during that time.")
                return render(request, 'booking/book_room.html', {'form': form})
            
            # --- 4. SAVE THE BOOKING ---
            new_booking.user = request.user 
            new_booking.save() 
            messages.success(request, "Booking request submitted successfully!")
            return redirect('my_bookings')
        else:
            # IF THE FORM FAILS VALIDATION
            print("--- FORM IS INVALID ---")
            print(form.errors)

    else:
        form = BookingForm()

    # --- NEW CODE TO PASS SCHEDULES TO HTML ---
    # Fetch ALL class schedules to send to the JavaScript
    all_schedules = ClassSchedule.objects.all()
    
    # Create a Python dictionary to send to JavaScript
    schedules_data = []
    for sched in all_schedules:
        schedules_data.append({
            'room_id': sched.room.id,
            'day': sched.day_of_week,
            'start': sched.start_time.strftime('%H:%M'),
            'end': sched.end_time.strftime('%H:%M'),
            'subject': sched.subject_name,
        })

    context = {
        'form': form,
        'schedules_json': schedules_data # Pass this to the template
    }
    return render(request, 'booking/book_room.html', context)

@user_passes_test(lambda u: u.is_staff)
@login_required
def approve_bookings(request):
    # Fetch only bookings with a PENDING status
    pending_bookings = Booking.objects.filter(status='PENDING')
    return render(request, 'booking/approve_bookings.html', {'bookings': pending_bookings})

@user_passes_test(lambda u: u.is_staff)
@login_required
def update_booking_status(request, booking_id, status):
    # Find the booking and change its status
    booking = Booking.objects.get(id=booking_id)
    booking.status = status
    booking.save()
    return redirect('approve_bookings')

@login_required
def my_bookings(request):
    # Get only the bookings belonging to the logged-in user, newest first
    bookings = Booking.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required
def cancel_booking(request, booking_id):
    # Find the specific booking
    booking = Booking.objects.get(id=booking_id)
    
    # Security check: Make sure the logged-in user actually owns this booking
    if booking.user == request.user:
        booking.status = 'CANCELLED'
        booking.save()
        messages.success(request, "Your booking has been cancelled.")
    else:
        messages.error(request, "You do not have permission to cancel this.")
        
    return redirect('my_bookings')