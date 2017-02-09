import midi

midi_file = 'pacman.mid'
start_pos = [0, 175, 25]
scale = 2

def makeNoteList(filename):
    pattern = midi.read_midifile(filename)
    time = 0
    notes = []
    for event in pattern[0]:
        if type(event) is midi.events.NoteOnEvent:
            time += event.tick
            if event.data[1] != 0:
                notes.append([event.data[0]-58, time/1200.*scale])
        elif type(event) is midi.events.NoteOffEvent:
            time += event.tick
    return notes

def generateAHK(notes):
    f = open('build_music.ahk','w')
    with open ("ahk_functions", "r") as funcs:
        output = funcs.read()
    for note in notes:
        output += 'clickPlus()\n'
        output += 'checkPlusMenu()\n'
        output += 'clickBall()\n'
        output += 'clickProperties()\n'
        output += 'clickSpawnOrder()\n'
        output += 'input('+str(note[0])+')\n'
        output += 'clickPosition()\n'
        output += 'clickField1()\n'
        output += 'input('+str(start_pos[0]+note[1])+')\n'
        output += 'clickField2()\n'
        output += 'input('+str(start_pos[1])+')\n'
        output += 'clickField3()\n'
        output += 'input('+str(start_pos[2])+')\n'
        output += 'if (pause_var1 = 1) {\n\tBlockInput MouseMoveOff\n\tPause On\n}\n'
        output += 'Sleep 500\n'
    output += 'BlockInput MouseMoveOff\n'
    output += 'time_elapsed := FormatSeconds((A_TickCount-StartTime)/1000)\n'
    output += 'MsgBox Build time:`n%time_elapsed%\n'
    output += 'ExitApp\n'
    output += 'F1::\nBlockInput MouseMoveOff\nExitApp\nreturn\n' # Sets F1 to terminate script
    output += 'F2::\nPause Off\nBlockInput MouseMove\nif (pause_var1 = 0)\n\tpause_var1 := 1\nelse\n\tpause_var1 := 0\nreturn\n' # Sets F2 to pause script when finished with current object
    output += 'F3::\nPause Off\nBlockInput MouseMove\nif (pause_var2 = 0) {\n\tpause_var2 := 1\n\tBlockInput MouseMoveOff\n\tPause On\n}\nelse\n\tpause_var2 := 0\nreturn\n' # Sets F3 to pause script immediately
    f.write(output)
    f.close()
    
def main():
    notes = makeNoteList(midi_file)
    generateAHK(notes)
    print "Success. Song contains", len(notes), "notes."
    
main()