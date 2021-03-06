import copy


INSTRUMENTS = {
        # MIDI instruments
        'Grand Piano'                   :[0, 'pno.'],
        'Acoustic Grand Piano'	        :[1, 'pno.'],
        'Bright Acoustic Piano'	        :[2, ''],
        'Electric Grand Piano'	        :[3, ''],
        'Honky-Tonk'	                :[4, ''],
        'Electric Piano 1'	            :[5, ''],
        'Electric Piano 2'	            :[6, ''],
        'Harpsichord'	                :[7, ''],
        'Clavinet'	                    :[8, ''],
        'elesta'	                    :[9, ''], # Interestingly it fails with this instrument #TODO: Check why
        'Glockenspiel'	                :[10, ''],
        'Music Box'	                    :[11, ''],
        'Vibraphone'	                :[12, ''],
        'Marimba'	                    :[13, ''],
        'Xylophone'	                    :[14, ''],
        'Tubular Bells'	                :[15, ''],
        'Dulcimer'	                    :[16, ''],
        'Drawbar Organ'	                :[17, ''],
        'Percussive Organ'	            :[18, ''],
        'Rock Organ'	                :[19, ''],
        'Church Organ'	                :[20, ''],
        'Reed Organ'	                :[21, ''],
        'Accordion'	                    :[22, 'acc.'],
        'Harmonica'	                    :[23, 'hca.'],
        'Tango Accordian'	            :[24, ''],
        'Acoustic Guitar(nylon)'        :[25, ''],
        'Acoustic Guitar(steel)'	    :[26, ''],
        'Electric Guitar(jazz)'	        :[27, ''],
        'Electric Guitar(clean)'        :[28, ''],
        'Electric Guitar(muted)'	    :[29, ''],
        'Overdriven Guitar'	            :[30, ''],
        'Distortion Guitar'	            :[31, ''],
        'Guitar Harmonics'	            :[32, ''],
        'Acoustic Bass'	                :[33, ''],
        'Electric Bass (finger)'        :[34, ''],
        'Electric Bass (pick)'	        :[35, ''],
        'Fretless Bass'	                :[36, ''],
        'Slap Bass 1'	                :[37, ''],
        'Slap Bass 2'	                :[38, ''],
        'Synth Bass 1'	                :[39, ''],
        'Synth Bass 2'	                :[40, ''],
        'Violin'	                    :[41, ''],
        'Viola'	                        :[42, ''],
        'Cello'	                        :[43, ''],
        'Contrabass'	                :[44, ''],
        'Tremolo Strings'	            :[45, ''],
        'Pizzicato Strings'	            :[46, ''],
        'Orchestral Strings'	        :[47, ''],
        'Timpani'	                    :[48, ''],
        'String Ensemble 1'	            :[49, ''],
        'String Ensemble 2'	            :[50, ''],
        'SynthStrings 1'	            :[51, ''],
        'SynthStrings 2'	            :[52, ''],
        'Choir Aahs'	                :[53, ''],
        'Voice Oohs'	                :[54, ''],
        'Synth Voice'	                :[55, ''],
        'Orchestra Hit'	                :[56, ''],
        'Trumpet'	                    :[57, ''],
        'Trombone'	                    :[58, ''],
        'Tuba'	                        :[59, ''],
        'Muted Trumpet'	                :[60, ''],
        'French Horn'	                :[61, ''],
        'Brass Section'	                :[62, ''],
        'SynthBrass 1'	                :[63, ''],
        'SynthBrass 2'	                :[64, ''],
        'Soprano Sax'	                :[65, ''],
        'Alto Sax'	                    :[66, ''],
        'Tenor Sax'	                    :[67, ''],
        'Baritone Sax'	                :[68, ''],
        'Oboe'	                        :[69, ''],
        'English Horn'	                :[70, ''],
        'Bassoon'	                    :[71, ''],
        'Clarinet'	                    :[72, ''],
        'Piccolo'	                    :[73, ''],
        'Flute'	                        :[74, ''],
        'Recorder'	                    :[75, ''],
        'Pan Flute'	                    :[76, ''],
        'Blown Bottle'	                :[77, ''],
        'Skakuhachi'	                :[78, ''],
        'Whistle'	                    :[79, ''],
        'Ocarina'	                    :[80, 'oca.'],
        'Lead 1 (square)'	            :[81, ''],
        'Lead 2 (sawtooth)'	            :[82, ''],
        'Lead 3 (calliope)'	            :[83, ''],
        'Lead 4 (chiff)'	            :[84, ''],
        'Lead 5 (charang)'	            :[85, ''],
        'Lead 6 (voice)'	            :[86, ''],
        'Lead 7 (fifths)'	            :[87, ''],
        'Lead 8 (bass+lead)'	        :[88, ''],
        'Pad 1 (new age)'	            :[89, ''],
        'Pad 2 (warm)'	                :[90, ''],
        'Pad 3 (polysynth)'	            :[91, ''],
        'Pad 4 (choir)'	                :[92, ''],
        'Pad 5 (bowed)'	                :[93, ''],
        'Pad 6 (metallic)'	            :[94, ''],
        'Pad 7 (halo)'	                :[95, ''],
        'Pad 8 (sweep)'	                :[96, ''],
        'FX 1 (rain)'	                :[97, ''],
        'FX 2 (soundtrack)'	            :[98, ''],
        'FX 3 (crystal)'	            :[99, ''],
        'FX 4 (atmosphere)'	            :[100, ''],
        'FX 5 (brightness)'	            :[101, ''],
        'FX 6 (goblins)'	            :[102, ''],
        'FX 7 (echoes)'	                :[103, ''],
        'FX 8 (sci-fi)'	                :[104, ''],
        'Sitar'	                        :[105, ''],
        'Banjo'	                        :[106, 'Bjo.'],
        'Shamisen'	                    :[107, ''],
        'Koto'	                        :[108, ''],
        'Kalimba'	                    :[109, ''],
        'Bagpipe'	                    :[110, ''],
        'Fiddle'	                    :[111, ''],
        'Shanai'	                    :[112, ''],
        'Tinkle Bell'	                :[113, ''],
        'Agogo'	                        :[114, ''],
        'Steel Drums'	                :[115, ''],
        'Woodblock'	                    :[116, ''],
        'Taiko Drum'	                :[117, ''],
        'Melodic Tom'	                :[118, ''],
        'Synth Drum'	                :[119, ''],
        'Reverse Cymbal'    	        :[120, ''],
        'Guitar Fret Noise'	            :[121, ''],
        'Breath Noise'	                :[122, ''],
        'Seashore'	                    :[123, ''],
        'Bird Tweet'	                :[124, ''],
        'Telephone Ring'	            :[125, ''],
        'Helicopter'	                :[126, ''],
        'Applause'	                    :[127, ''],
        'Gunshot'	                    :[128, '']
}

PERCUSSION = {
        'Bass Drum 2'			:[35, ''],
        'Bass Drum 1'			:[36, ''],
        'Side Stick'			:[37, ''],
        'Snare Drum 1'			:[38, ''],
        'Hand Clap'			    :[39, ''],
        'Snare Drum 2'			:[40, ''],
        'Low Tom 2'			    :[41, ''],
        'Closed Hi-hat'			:[42, ''],
        'Low Tom 1'			    :[43, ''],
        'Pedal Hi-hat'			:[44, ''],
        'Mid Tom 2'			    :[45, ''],
        'Open Hi-hat'			:[46, ''],
        'Mid Tom 1'			    :[47, ''],
        'High Tom 2'			:[48, ''],
        'Crash Cymbal 1'		:[49, ''],
        'High Tom 1'			:[50, ''],
        'Ride Cymbal 1'			:[51, ''],
        'Chinese Cymbal'		:[52, ''],
        'Ride Bell'			    :[53, ''],
        'Tambourine'			:[54, ''],
        'Splash Cymbal'			:[55, ''],
        'Cowbell'			    :[56, ''],
        'Crash Cymbal 2'		:[57, ''],
        'Vibra Slap'			:[58, ''],
        'Ride Cymbal 2'			:[59, ''],
        'High Bongo'			:[60, ''], # Here to 65 like african drums and snares
        'Low Bongo'			    :[61, ''],
        'Mute High Conga'		:[62, ''],
        'Open High Conga'		:[63, ''],
        'Low Conga'			    :[64, ''],
        'High Timbale'			:[65, ''],
        'Low Timbale'			:[66, ''], # Like snare
        'High Agogo'			:[67, ''], # goung gong
        'Low Agogo'			    :[68, ''], # like goung gong
        'Cabasa'			    :[69, ''], # like checkere
        'Maracas'			    :[70, ''], # Good for fill. Checkere
        'Short Whistle'			:[71, ''],
        'Long Whistle'			:[72, ''],
        'Short Guiro'			:[73, ''],
        'Long Guiro'			:[74, ''],
        'Claves'			    :[75, ''], # Also sounds good for fill. Sounds like the wood block from birocol (tuc tuc tuc - tuc tuc)
        'High Wood Block'		:[76, ''],
        'Low Wood Block'		:[77, ''], # Wood block is good for fill
        'Mute Cuica'			:[78, ''],
        'Open Cuica'			:[79, ''],
        'Mute Triangle'			:[80, ''],
        'Open Triangle'			:[81, '']
}


class InstrumentEnums(object):

    def __init__(self):
        for instr in INSTRUMENTS:
            name = copy.deepcopy(instr)
            instr = instr.replace('(', ' ').replace(')', '').strip()
            instr = instr.replace('  ', '_').replace(' ', '_')
            instr = instr.replace('-', '_').upper()
            setattr(self, instr, name)


class PercussionEnums(object):

    def __init__(self):
        for instr in PERCUSSION:
            name = copy.deepcopy(instr)
            instr = instr.replace('(', ' ').replace(')', '').strip()
            instr = instr.replace('  ', '_').replace(' ', '_')
            instr = instr.replace('-', '_').upper()
            setattr(self, instr, name)