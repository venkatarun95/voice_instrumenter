Read from file... /home/venkat/Documents/Projects/Farzi/music/tmp.wav
select all
sound = selected ("Sound")
select sound
tmin = Get start time
tmax = Get end time
To Pitch... 0 75 300
Rename... "pitch"
select sound
To Intensity... 75 0.001
Rename... "intensity"\
for i to (tmax-tmin)/0.01
    time = tmin + i * 0.01
    select all
    pitch = selected("Pitch")
    intensity = selected("Intensity")
    select pitch
    pitch = Get value at time... 'time' Hertz Linear
    select intensity
    intensity = Get value at time... 'time' Cubic
    fileappend /home/venkat/Documents/Projects/Farzi/music/out.txt 'time:2' 'pitch:3' 'intensity:3' 'newline$'
#appendInfoLine... 'fixed$' (time, 2) " " 'fixed$' (pitch, 3) " " fixed$ (intensity, 3)
endfor
