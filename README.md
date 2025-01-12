# Vocal Studio

Starting a project to create an AI voice assistant to control ableton.

Ideally, this can be used to:
- Create songs
- Mix and add effect chains to tracks
- Create sounds with native and plugin synthesizers

## Approach

- OpenAI whisper to transcribe audio to text prompts
- Use text prompts 

## Dev reference 
Alright, It's fucked. Going to try and reverse engineer the ableton midi remote script api.

First, downloading a python decompiler on windows. 

Need to get make first

```powershell
choco install make
```

This is godsend, someone decompiled the live 12 Midi remote scripts https://github.com/gluon/AbletonLive12_MIDIRemoteScripts.

I'm trying to reverse engineer an understanding of the `Subject` lifecycle. Primarily through an Ableton Live 12 `ControlSurface` object. 

So far I have determined that:
- The constructor is invoked when the control surface is added to the midi map in Preferences > Link, Tempo & MIDI
- The `disconnect` method is invoked when the control surface is removed from the midi map in Preferences > Link, Tempo & MIDI
