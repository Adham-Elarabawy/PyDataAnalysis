# author: Adham Elarabawy
import matplotlib.pyplot as plt
import time
import datetime as dt

# constants
k = 9 * 10 ^ 9
q1 = 1.6 * 1/(10 ^ 19)  # pos
q2 = q1  # neg
posColor = '#1f77b4'
negColor = '#d62728'
# some negligible mass. Can change if needed. Affects calculated acceleration.
mass = 1
arrowAmp = 0.25  # changes force scaling factor for the vectors (purely visual)
granularity = 0.01  # increase to have smoother animation. more computation though


# init variables
q1_pos = 0.25
q2_pos = 1

q1_vel = 0
q2_vel = 0

left_bound_screen = 0
right_bound_screen = 2

forces = []
distances = []

plt.ion()
fig, ax = plt.subplots()
x, y = [[q1_pos, q2_pos], [0, 0]]
a1 = ax.arrow(q1_pos, 0, 0, 0, head_width=0.01,
              head_length=0.05, fc=posColor, ec=posColor)
a2 = ax.arrow(q2_pos, 0, 0, 0, head_width=0.01,
              head_length=0.05, fc=negColor, ec=negColor)
sc = ax.scatter(x, y, c="black")
plt.xlim(left_bound_screen, right_bound_screen)
plt.ylim(-0.5, 2)
plt.title("Stationary Charge Simulation")
plt.xlabel("distance (m)")
plt.ylabel("force (N)")
plt.draw()

q1_accel = 1
q2_accel = 1

collided = False
while not collided:
    if(q1_pos > q2_pos) or (((q1_pos < left_bound_screen) or (q1 > right_bound_screen)) and ((q2_pos > right_bound_screen) or (q2_pos < left_bound_screen))):
        print('simulation terminated: end condition reached')
        collided = True
    a_time = dt.datetime.now()
    force = k * abs(q1) * abs(q2) / ((q2_pos - q1_pos) * (q2_pos - q1_pos))
    forces.append(force)
    distances.append(q2_pos-q1_pos)
    acceleration = force / mass
    if((q1 > 0) == (q2 > 0)):  # both charges are the same sign
        if(q1_pos < q2_pos):  # if q1 is to the left of q2
            q1_vel -= acceleration * granularity
            q1_pos += q1_vel * granularity
            q1_accel = -1

            q2_vel += acceleration * granularity
            q2_pos += q2_vel * granularity
            q2_accel = 1
        else:  # if q2 is to the left of q1
            q2_vel -= acceleration * granularity
            q2_pos += q2_vel * granularity
            q2_accel = -1

            q1_vel += acceleration * granularity
            q1_pos += q1_vel * granularity
            q1_accel = 1
    else:  # both charges are different signs
        if(q1_pos < q2_pos):  # if q1 is to the left of q2
            q1_vel += acceleration * granularity
            q1_pos += q1_vel * granularity
            q1_accel = 1

            q2_vel -= acceleration * granularity
            q2_pos += q2_vel * granularity
            q2_accel = -1
        else:  # if q2 is to the left of q1
            q2_vel += acceleration * granularity
            q2_pos += q2_vel * granularity
            q2_accel = 1

            q1_vel -= acceleration * granularity
            q1_pos += q1_vel * granularity
            q1_accel = -1

    print('q1_pos: [' + str(q1_pos) + '], q2_pos: [' + str(q2_pos) + '], force: [' +
          str(force) + '], distance: [' + str(q2_pos - q1_pos) + ']', end='\r')
    b_time = dt.datetime.now()
    time_elapsed = (b_time-a_time).total_seconds()
    x, y = [[q1_pos, q2_pos], [0, 0]]

    sc.remove()
    a1.remove()
    a2.remove()

    a1 = ax.arrow(q1_pos, 0, q1_accel*force*arrowAmp, 0, head_width=0.03,
                  head_length=0.05, fc=posColor, ec=posColor)
    a2 = ax.arrow(q2_pos, 0, q2_accel*force*arrowAmp, 0, head_width=0.03,
                  head_length=0.05, fc=negColor, ec=negColor)

    sc = plt.scatter(x, y, color='black')
    timeseries = ax.plot(distances, forces, color='#9467bd')

    if(granularity > time_elapsed):
        plt.pause(granularity - time_elapsed)
    fig.canvas.draw_idle()
