import pygame
import serial

# Initialize pygame and set up the display window
pygame.init()
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Joystick-Controlled Circle Game")

# Connect to the serial port for the joystick input
ser = serial.Serial('COM8', 9600)  # Replace 'COM8' with your Arduino port

# Circle properties
circle_radius = 20
circle_x, circle_y = win_width // 2, win_height // 2  # Start in the center of the screen
circle_color = (0, 0, 255)
speed_modifier = 0.05  # Adjust this value to control sensitivity

# Run the main game loop
running = True
while running:
    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Read data from the serial port
    data = ser.readline().decode().strip().split(',')
    if len(data) == 3:
        try:
            joy_x, joy_y, button_state = map(int, data)
            print(f"X: {joy_x}, Y: {joy_y}, Button: {button_state}")

            # Map joystick values to circle movement
            # Here, we assume joystick values are in the range 0-1023, adjust if necessary
            if joy_x < 400:  # Threshold for left movement
                circle_x -= speed_modifier * (400 - joy_x)
            elif joy_x > 600:  # Threshold for right movement
                circle_x += speed_modifier * (joy_x - 600)

            if joy_y < 400:  # Threshold for up movement
                circle_y -= speed_modifier * (400 - joy_y)
            elif joy_y > 600:  # Threshold for down movement
                circle_y += speed_modifier * (joy_y - 600)

            # Ensure the circle stays within the window bounds
            circle_x = max(circle_radius, min(circle_x, win_width - circle_radius))
            circle_y = max(circle_radius, min(circle_y, win_height - circle_radius))

        except ValueError:
            print("Error in parsing joystick data.")

    # Fill the window with a white background
    win.fill((255, 255, 255))

    # Draw the circle at the updated position
    pygame.draw.circle(win, circle_color, (int(circle_x), int(circle_y)), circle_radius)

    # Update the display
    pygame.display.flip()

# Close the serial port and quit pygame
ser.close()
pygame.quit()
