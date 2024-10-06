{\rtf1\ansi\ansicpg1252\cocoartf1561\cocoasubrtf400
{\fonttbl\f0\fnil\fcharset0 LucidaGrande;\f1\fnil\fcharset178 GeezaPro;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww13260\viewh10200\viewkind0
\pard\tqr\tx566\tqr\tx1133\tqr\tx1700\tqr\tx2267\tqr\tx2834\tqr\tx3401\tqr\tx3968\tqr\tx4535\tqr\tx5102\tqr\tx5669\tqr\tx6236\tqr\tx6803\pardirnatural\qr\partightenfactor0

\f0\fs24 \cf0 import
\f1  
\f0 streamlit
\f1  
\f0 as
\f1  
\f0 st
\f1 \

\f0 import
\f1  
\f0 librosa
\f1 \

\f0 import
\f1  
\f0 librosa
\f1 .
\f0 display
\f1 \

\f0 import
\f1  
\f0 matplotlib
\f1 .
\f0 pyplot
\f1  
\f0 as
\f1  
\f0 plt
\f1 \

\f0 import
\f1  
\f0 numpy
\f1  
\f0 as
\f1  
\f0 np
\f1 \

\f0 from
\f1  
\f0 io
\f1  
\f0 import
\f1  
\f0 BytesIO
\f1 \
\

\f0 #
\f1  
\f0 Function
\f1  
\f0 to
\f1  
\f0 format
\f1  
\f0 time
\f1  
\f0 in
\f1  
\f0 HH:MM:SS
\f1 \

\f0 def
\f1  
\f0 format_time(seconds):
\f1 \
    
\f0 hours
\f1  
\f0 =
\f1  
\f0 int(seconds
\f1  
\f0 //
\f1  
\f0 3600)
\f1 \
    
\f0 minutes
\f1  
\f0 =
\f1  
\f0 int((seconds
\f1  
\f0 %
\f1  
\f0 3600)
\f1  
\f0 //
\f1  
\f0 60)
\f1 \
    
\f0 secs
\f1  
\f0 =
\f1  
\f0 seconds
\f1  
\f0 %
\f1  
\f0 60
\f1 \
    
\f0 return
\f1  
\f0 f'\{hours:02d\}:\{minutes:02d\}:\{secs:06
\f1 .
\f0 3f\}'
\f1 \
\

\f0 #
\f1  
\f0 Function
\f1  
\f0 to
\f1  
\f0 detect
\f1  
\f0 audio
\f1  
\f0 dropouts
\f1 \

\f0 def
\f1  
\f0 detect_dropouts(file_data,
\f1  
\f0 dropout_db_threshold=-20,
\f1  
\f0 min_duration_ms=100):
\f1 \
    
\f0 #
\f1  
\f0 Load
\f1  
\f0 the
\f1  
\f0 audio
\f1  
\f0 file
\f1 \
    
\f0 y,
\f1  
\f0 sr
\f1  
\f0 =
\f1  
\f0 librosa
\f1 .
\f0 load(file_data,
\f1  
\f0 sr=None)
\f1 \
\
    
\f0 #
\f1  
\f0 Improved
\f1  
\f0 time
\f1  
\f0 resolution
\f1  
\f0 by
\f1  
\f0 reducing
\f1  
\f0 hop
\f1  
\f0 length
\f1 \
    
\f0 hop_length
\f1  
\f0 =
\f1  
\f0 256
\f1   
\f0 #
\f1  
\f0 Reduced
\f1  
\f0 hop
\f1  
\f0 length
\f1  
\f0 for
\f1  
\f0 better
\f1  
\f0 time
\f1  
\f0 resolution
\f1 \
    
\f0 frame_length
\f1  
\f0 =
\f1  
\f0 hop_length
\f1  
\f0 /
\f1  
\f0 sr
\f1  
\f0 *
\f1  
\f0 1000
\f1   
\f0 #
\f1  
\f0 ms
\f1  
\f0 per
\f1  
\f0 frame
\f1 \
\
    
\f0 #
\f1  
\f0 Convert
\f1  
\f0 the
\f1  
\f0 signal
\f1  
\f0 to
\f1  
\f0 decibels
\f1 \
    
\f0 rms
\f1  
\f0 =
\f1  
\f0 librosa
\f1 .
\f0 feature
\f1 .
\f0 rms(y=y,
\f1  
\f0 frame_length=hop_length,
\f1  
\f0 hop_length=hop_length)
\f1 \
    
\f0 rms_db
\f1  
\f0 =
\f1  
\f0 librosa
\f1 .
\f0 power_to_db(rms,
\f1  
\f0 ref=np
\f1 .
\f0 max)
\f1 \
\
    
\f0 #
\f1  
\f0 Threshold
\f1  
\f0 to
\f1  
\f0 find
\f1  
\f0 dropouts
\f1  
\f0 (segments
\f1  
\f0 below
\f1  
\f0 the
\f1  
\f0 dropout_db_threshold)
\f1 \
    
\f0 dropout_frames
\f1  
\f0 =
\f1  
\f0 rms_db[0]
\f1  
\f0 <
\f1  
\f0 dropout_db_threshold
\f1 \
\
    
\f0 #
\f1  
\f0 Detect
\f1  
\f0 contiguous
\f1  
\f0 frames
\f1  
\f0 of
\f1  
\f0 dropouts
\f1  
\f0 lasting
\f1  
\f0 at
\f1  
\f0 least
\f1  
\f0 min_duration_ms
\f1 \
    
\f0 min_frames
\f1  
\f0 =
\f1  
\f0 int(min_duration_ms
\f1  
\f0 /
\f1  
\f0 frame_length)
\f1 \
    
\f0 dropouts
\f1  
\f0 =
\f1  
\f0 []
\f1 \
    
\f0 start
\f1  
\f0 =
\f1  
\f0 None
\f1 \
\
    
\f0 for
\f1  
\f0 i,
\f1  
\f0 is_dropout
\f1  
\f0 in
\f1  
\f0 enumerate(dropout_frames):
\f1 \
        
\f0 if
\f1  
\f0 is_dropout
\f1  
\f0 and
\f1  
\f0 start
\f1  
\f0 is
\f1  
\f0 None:
\f1 \
            
\f0 start
\f1  
\f0 =
\f1  
\f0 i
\f1   
\f0 #
\f1  
\f0 Start
\f1  
\f0 of
\f1  
\f0 a
\f1  
\f0 dropout
\f1 \
        
\f0 elif
\f1  
\f0 not
\f1  
\f0 is_dropout
\f1  
\f0 and
\f1  
\f0 start
\f1  
\f0 is
\f1  
\f0 not
\f1  
\f0 None:
\f1 \
            
\f0 if
\f1  
\f0 i
\f1  
\f0 -
\f1  
\f0 start
\f1  
\f0 >=
\f1  
\f0 min_frames:
\f1 \
                
\f0 start_time
\f1  
\f0 =
\f1  
\f0 start
\f1  
\f0 *
\f1  
\f0 hop_length
\f1  
\f0 /
\f1  
\f0 sr
\f1 \
                
\f0 end_time
\f1  
\f0 =
\f1  
\f0 i
\f1  
\f0 *
\f1  
\f0 hop_length
\f1  
\f0 /
\f1  
\f0 sr
\f1 \
                
\f0 duration_ms
\f1  
\f0 =
\f1  
\f0 (end_time
\f1  
\f0 -
\f1  
\f0 start_time)
\f1  
\f0 *
\f1  
\f0 1000
\f1   
\f0 #
\f1  
\f0 Convert
\f1  
\f0 duration
\f1  
\f0 to
\f1  
\f0 milliseconds
\f1 \
                
\f0 dropouts
\f1 .
\f0 append((start_time,
\f1  
\f0 end_time,
\f1  
\f0 duration_ms))
\f1 \
            
\f0 start
\f1  
\f0 =
\f1  
\f0 None
\f1 \
\
    
\f0 #
\f1  
\f0 Handle
\f1  
\f0 the
\f1  
\f0 case
\f1  
\f0 where
\f1  
\f0 dropout
\f1  
\f0 extends
\f1  
\f0 to
\f1  
\f0 the
\f1  
\f0 end
\f1  
\f0 of
\f1  
\f0 the
\f1  
\f0 file
\f1 \
    
\f0 if
\f1  
\f0 start
\f1  
\f0 is
\f1  
\f0 not
\f1  
\f0 None
\f1  
\f0 and
\f1  
\f0 len(dropout_frames)
\f1  
\f0 -
\f1  
\f0 start
\f1  
\f0 >=
\f1  
\f0 min_frames:
\f1 \
        
\f0 start_time
\f1  
\f0 =
\f1  
\f0 start
\f1  
\f0 *
\f1  
\f0 hop_length
\f1  
\f0 /
\f1  
\f0 sr
\f1 \
        
\f0 end_time
\f1  
\f0 =
\f1  
\f0 len(dropout_frames)
\f1  
\f0 *
\f1  
\f0 hop_length
\f1  
\f0 /
\f1  
\f0 sr
\f1 \
        
\f0 duration_ms
\f1  
\f0 =
\f1  
\f0 (end_time
\f1  
\f0 -
\f1  
\f0 start_time)
\f1  
\f0 *
\f1  
\f0 1000
\f1 \
        
\f0 dropouts
\f1 .
\f0 append((start_time,
\f1  
\f0 end_time,
\f1  
\f0 duration_ms))
\f1 \
\
    
\f0 return
\f1  
\f0 dropouts,
\f1  
\f0 y,
\f1  
\f0 sr
\f1 \
\

\f0 #
\f1  
\f0 Function
\f1  
\f0 to
\f1  
\f0 plot
\f1  
\f0 waveform
\f1  
\f0 with
\f1  
\f0 dropouts
\f1 \

\f0 def
\f1  
\f0 plot_waveform_with_dropouts(y,
\f1  
\f0 sr,
\f1  
\f0 dropouts):
\f1 \
    
\f0 plt
\f1 .
\f0 figure(figsize=(12,
\f1  
\f0 6))
\f1 \
    
\f0 librosa
\f1 .
\f0 display
\f1 .
\f0 waveshow(y,
\f1  
\f0 sr=sr,
\f1  
\f0 alpha=0
\f1 .
\f0 6)
\f1 \
    
\f0 plt
\f1 .
\f0 title('Waveform
\f1  
\f0 with
\f1  
\f0 Detected
\f1  
\f0 Dropouts')
\f1 \
    
\f0 plt
\f1 .
\f0 xlabel('Time
\f1  
\f0 (seconds)')
\f1 \
    
\f0 plt
\f1 .
\f0 ylabel('Amplitude')
\f1 \
\
    
\f0 #
\f1  
\f0 Highlight
\f1  
\f0 dropouts
\f1 \
    
\f0 for
\f1  
\f0 dropout
\f1  
\f0 in
\f1  
\f0 dropouts:
\f1 \
        
\f0 start_time,
\f1  
\f0 end_time,
\f1  
\f0 _
\f1  
\f0 =
\f1  
\f0 dropout
\f1 \
        
\f0 plt
\f1 .
\f0 axvspan(start_time,
\f1  
\f0 end_time,
\f1  
\f0 color='red',
\f1  
\f0 alpha=0
\f1 .
\f0 5,
\f1  
\f0 label='Dropout'
\f1  
\f0 if
\f1  
\f0 'Dropout'
\f1  
\f0 not
\f1  
\f0 in
\f1  
\f0 plt
\f1 .
\f0 gca()
\f1 .
\f0 get_legend_handles_labels()[1]
\f1  
\f0 else
\f1  
\f0 "")
\f1 \
    \
    
\f0 plt
\f1 .
\f0 legend()
\f1 \
    
\f0 st
\f1 .
\f0 pyplot(plt)
\f1 \
\

\f0 #
\f1  
\f0 Streamlit
\f1  
\f0 app
\f1  
\f0 layout
\f1 \

\f0 st
\f1 .
\f0 title("Audio
\f1  
\f0 Dropout
\f1  
\f0 Detection")
\f1 \

\f0 st
\f1 .
\f0 write("Upload
\f1  
\f0 an
\f1  
\f0 audio
\f1  
\f0 file
\f1  
\f0 (WAV
\f1  
\f0 format)
\f1  
\f0 to
\f1  
\f0 detect
\f1  
\f0 dropouts
\f1  
\f0 in
\f1  
\f0 the
\f1  
\f0 audio
\f1  
\f0 signal
\f1 .
\f0 ")
\f1 \
\

\f0 #
\f1  
\f0 Upload
\f1  
\f0 audio
\f1  
\f0 file
\f1 \

\f0 audio_file
\f1  
\f0 =
\f1  
\f0 st
\f1 .
\f0 file_uploader("Choose
\f1  
\f0 an
\f1  
\f0 audio
\f1  
\f0 file",
\f1  
\f0 type=["wav"])
\f1 \
\

\f0 if
\f1  
\f0 audio_file
\f1  
\f0 is
\f1  
\f0 not
\f1  
\f0 None:
\f1 \
    
\f0 #
\f1  
\f0 Process
\f1  
\f0 the
\f1  
\f0 uploaded
\f1  
\f0 file
\f1 \
    
\f0 st
\f1 .
\f0 audio(audio_file,
\f1  
\f0 format='audio/wav')
\f1 \
    
\f0 dropouts,
\f1  
\f0 y,
\f1  
\f0 sr
\f1  
\f0 =
\f1  
\f0 detect_dropouts(audio_file)
\f1 \
\
    
\f0 #
\f1  
\f0 Display
\f1  
\f0 detected
\f1  
\f0 dropouts
\f1  
\f0 in
\f1  
\f0 a
\f1  
\f0 table
\f1 \
    
\f0 st
\f1 .
\f0 subheader("Detected
\f1  
\f0 Dropouts")
\f1 \
    
\f0 if
\f1  
\f0 dropouts:
\f1 \
        
\f0 for
\f1  
\f0 dropout
\f1  
\f0 in
\f1  
\f0 dropouts:
\f1 \
            
\f0 start,
\f1  
\f0 end,
\f1  
\f0 duration_ms
\f1  
\f0 =
\f1  
\f0 dropout
\f1 \
            
\f0 st
\f1 .
\f0 write(f"Start:
\f1  
\f0 \{format_time(start)\}
\f1  
\f0 |
\f1  
\f0 End:
\f1  
\f0 \{format_time(end)\}
\f1  
\f0 |
\f1  
\f0 Duration:
\f1  
\f0 \{duration_ms:
\f1 .
\f0 0f\}
\f1  
\f0 ms")
\f1 \
    
\f0 else:
\f1 \
        
\f0 st
\f1 .
\f0 write("No
\f1  
\f0 significant
\f1  
\f0 dropouts
\f1  
\f0 detected
\f1 .
\f0 ")
\f1 \
    \
    
\f0 #
\f1  
\f0 Plot
\f1  
\f0 waveform
\f1  
\f0 with
\f1  
\f0 highlighted
\f1  
\f0 dropouts
\f1 \
    
\f0 st
\f1 .
\f0 subheader("Waveform
\f1  
\f0 with
\f1  
\f0 Dropouts")
\f1 \
    
\f0 plot_waveform_with_dropouts(y,
\f1  
\f0 sr,
\f1  
\f0 dropouts)
\f1 \
}