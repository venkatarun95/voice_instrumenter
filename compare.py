import os
import sys

import main

if __name__ == "__main__":
    # Args:
    # reference_wav_file user_wav_file

    os.system("rm out.txt")
    os.system('touch out.txt')
    os.system("cp " + sys.argv[1] + " tmp.wav")
    os.system("praat listing.praat 60 \"yes\" 0 75 600")
    ref = main.read_music_file('out.txt')

    os.system("rm out.txt")
    os.system('touch out.txt')
    os.system("cp " + sys.argv[2] + " tmp.wav")
    os.system("praat listing.praat 60 \"yes\" 0 75 600")
    usr = main.read_music_file('out.txt')

    ref_data = map(lambda x: (0, x[1])[x[1] != None], ref)
    usr_data = map(lambda x: (0, x[1])[x[1] != None], usr)
    time = map(lambda x:x[0], usr)
    if len(ref_data) > len(usr_data):
        ref_data = usr_data[:len(usr_data)]
    assert(len(ref_data) <= len(usr_data))

    print '''
data = {
  labels: '''+str(time)+'''
  datasets: [
    {
      label: "You",
      fillColor: "rgba(220,220,220,0.2)",
      strokeColor: "rgba(220,220,220,1)",
      pointColor: "rgba(220,220,220,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(220,220,220,1)",
      data: '''+str(usr_data)+'''
    },
    {
      label: "Reference",
      fillColor: "rgba(151,187,205,0.2)",
      strokeColor: "rgba(151,187,205,1)",
      pointColor: "rgba(151,187,205,1)",
      pointStrokeColor: "#fff",
      pointHighlightFill: "#fff",
      pointHighlightStroke: "rgba(151,187,205,1)",
      data: '''+str(ref_data)+'''
    }
  ]
}
    '''
