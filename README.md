# Vocal Studio

Starting a project to create an AI voice assistant to control Ableton.

Ideally, this can be used to:
- Create songs
- Mix and add effect chains to tracks
- Create sounds with native and plugin synthesizers

## Approach
I'm testing this against Ableton Live 12.1.5 Suite.
I'm opting to use the MIDI Remote Script "API" because I want the full surface area of Ableton control commands.

Tragically, the MIDI Remote Script (MRS) environment and API is not public knowledge. We have to decompile
the builtin MRS control surface scripts and try and reverse engineer what's going on. :( 

The high level architecture is:

- User voice input.
- OpenAI whisper to transcribe audio to text prompts.
- NLP pruning to reduce language complexity.
- Text promts to language model (?).
- Language models to set of high level Ableton control commands.
- HTTP Client to send control commands.
- Ableton Control Surface running HTTP server to receive control commands.
- Ableton Control.

## Dev reference 
Alright, It's fucked. Going to try and reverse engineer the ableton midi remote script api.

I was having some trouble decompiling because of python version and some windows shenanigans, but these nerds got me.
Someone decompiled the live 12 Midi remote scripts https://github.com/gluon/AbletonLive12_MIDIRemoteScripts.

I'm trying to reverse engineer an understanding of the `Subject` lifecycle. Primarily through an Ableton Live 12 `ControlSurface` object. 

So far I have determined that:
- The constructor is invoked when the control surface is added to the midi map in Preferences > Link, Tempo & MIDI
- The `disconnect` method is invoked when the control surface is removed from the midi map in Preferences > Link, Tempo & MIDI

Printing out the method names of `c_instance` gives us some insight into what Ableton exposes to the midi control scripts (ignoring the internal dunder methods).

```python
'__bool__', '__class__', '__delattr__', '__dir__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'handle', 'instance_identifier', 'log_message', 'preferences', 'release_controlled_track', 'request_rebuild_midi_map', 'reset_input_history', 'send_midi', 'set_cc_translation', 'set_controlled_track', 'set_feedback_channels', 'set_feedback_velocity', 'set_note_translation', 'set_pad_translation', 'set_session_highlight', 'show_message', 'song', 'toggle_lock', 'update_locks'
```
Also printed out all the method names on `c_instance.song()`
```python
['View', '__bool__', '__class__', '__delattr__', '__dir__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__', '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', 'add_appointed_device_listener', 'add_arrangement_overdub_listener', 'add_back_to_arranger_listener', 'add_can_capture_midi_listener', 'add_can_jump_to_next_cue_listener', 'add_can_jump_to_prev_cue_listener', 'add_clip_trigger_quantization_listener', 'add_count_in_duration_listener', 'add_cue_points_listener', 'add_current_song_time_listener', 'add_data_listener', 'add_exclusive_arm_listener', 'add_groove_amount_listener', 'add_is_ableton_link_enabled_listener', 'add_is_ableton_link_start_stop_sync_enabled_listener', 'add_is_counting_in_listener', 'add_is_playing_listener', 'add_loop_length_listener', 'add_loop_listener', 'add_loop_start_listener', 'add_metronome_listener', 'add_midi_recording_quantization_listener', 'add_nudge_down_listener', 'add_nudge_up_listener', 'add_overdub_listener', 'add_punch_in_listener', 'add_punch_out_listener', 'add_re_enable_automation_enabled_listener', 'add_record_mode_listener', 'add_return_tracks_listener', 'add_root_note_listener', 'add_scale_information_listener', 'add_scale_intervals_listener', 'add_scale_mode_listener', 'add_scale_name_listener', 'add_scenes_listener', 'add_session_automation_record_listener', 'add_session_record_listener', 'add_session_record_status_listener', 'add_signature_denominator_listener', 'add_signature_numerator_listener', 'add_song_length_listener', 'add_start_time_listener', 'add_swing_amount_listener', 'add_tempo_follower_enabled_listener', 'add_tempo_listener', 'add_tracks_listener', 'add_tuning_system_listener', 'add_visible_tracks_listener', 'appointed_device_has_listener', 'arrangement_overdub_has_listener', 'back_to_arranger_has_listener', 'begin_undo_step', 'can_capture_midi_has_listener', 'can_jump_to_next_cue_has_listener', 'can_jump_to_prev_cue_has_listener', 'capture_and_insert_scene', 'capture_midi', 'clip_trigger_quantization_has_listener', 'continue_playing', 'count_in_duration_has_listener', 'create_audio_track', 'create_midi_track', 'create_return_track', 'create_scene', 'cue_points_has_listener', 'current_song_time_has_listener', 'data_has_listener', 'delete_return_track', 'delete_scene', 'delete_track', 'duplicate_scene', 'duplicate_track', 'end_undo_step', 'exclusive_arm_has_listener', 'find_device_position', 'force_link_beat_time', 'get_beats_loop_length', 'get_beats_loop_start', 'get_current_beats_song_time', 'get_current_smpte_song_time', 'get_data', 'groove_amount_has_listener', 'is_ableton_link_enabled_has_listener', 'is_ableton_link_start_stop_sync_enabled_has_listener', 'is_counting_in_has_listener', 'is_cue_point_selected', 'is_playing_has_listener', 'jump_by', 'jump_to_next_cue', 'jump_to_prev_cue', 'loop_has_listener', 'loop_length_has_listener', 'loop_start_has_listener', 'metronome_has_listener', 'midi_recording_quantization_has_listener', 'move_device', 'nudge_down_has_listener', 'nudge_up_has_listener', 'overdub_has_listener', 'play_selection', 'punch_in_has_listener', 'punch_out_has_listener', 're_enable_automation', 're_enable_automation_enabled_has_listener', 'record_mode_has_listener', 'redo', 'remove_appointed_device_listener', 'remove_arrangement_overdub_listener', 'remove_back_to_arranger_listener', 'remove_can_capture_midi_listener', 'remove_can_jump_to_next_cue_listener', 'remove_can_jump_to_prev_cue_listener', 'remove_clip_trigger_quantization_listener', 'remove_count_in_duration_listener', 'remove_cue_points_listener', 'remove_current_song_time_listener', 'remove_data_listener', 'remove_exclusive_arm_listener', 'remove_groove_amount_listener', 'remove_is_ableton_link_enabled_listener', 'remove_is_ableton_link_start_stop_sync_enabled_listener', 'remove_is_counting_in_listener', 'remove_is_playing_listener', 'remove_loop_length_listener', 'remove_loop_listener', 'remove_loop_start_listener', 'remove_metronome_listener', 'remove_midi_recording_quantization_listener', 'remove_nudge_down_listener', 'remove_nudge_up_listener', 'remove_overdub_listener', 'remove_punch_in_listener', 'remove_punch_out_listener', 'remove_re_enable_automation_enabled_listener', 'remove_record_mode_listener', 'remove_return_tracks_listener', 'remove_root_note_listener', 'remove_scale_information_listener', 'remove_scale_intervals_listener', 'remove_scale_mode_listener', 'remove_scale_name_listener', 'remove_scenes_listener', 'remove_session_automation_record_listener', 'remove_session_record_listener', 'remove_session_record_status_listener', 'remove_signature_denominator_listener', 'remove_signature_numerator_listener', 'remove_song_length_listener', 'remove_start_time_listener', 'remove_swing_amount_listener', 'remove_tempo_follower_enabled_listener', 'remove_tempo_listener', 'remove_tracks_listener', 'remove_tuning_system_listener', 'remove_visible_tracks_listener', 'return_tracks_has_listener', 'root_note_has_listener', 'scale_information_has_listener', 'scale_intervals_has_listener', 'scale_mode_has_listener', 'scale_name_has_listener', 'scenes_has_listener', 'scrub_by', 'session_automation_record_has_listener', 'session_record_has_listener', 'session_record_status_has_listener', 'set_data', 'set_or_delete_cue', 'signature_denominator_has_listener', 'signature_numerator_has_listener', 'song_length_has_listener', 'start_playing', 'start_time_has_listener', 'stop_all_clips', 'stop_playing', 'swing_amount_has_listener', 'tap_tempo', 'tempo_follower_enabled_has_listener', 'tempo_has_listener', 'tracks_has_listener', 'trigger_session_record', 'tuning_system_has_listener', 'undo', 'visible_tracks_has_listener']
```


Small tradgedy struck, but we're passed that. On the BaseHTTPRequestHandler I made a `log_message` method to forward prints to the ableton `c_instance.log_message` method...
which also happens to be an actual method on the handler lol. Took me like 2 hours to figure out why it was freezing because I need to swallow stderr since it's overridden in ableton. Fuck my life dude.
Ended up ripping out the server code to test locally (which I arguably should have been doing in the first place). Immediately I saw the error and was engulfed in rage.
