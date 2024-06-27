#!/bin/sh
#
# The receiver side processing is illustrated below
# The SCReAM receiver application receives multiplexed RTP media on port $2
#  and transits RTCP feedback over the same port
# The received RTP media is demultiplexed and forwarded on local
#  ports 30112, 30114, 31016 and 30118
# The video decoding assumes an NVIDIA Jetson Nano or Xavier NX platform, change to applicable
#  HW decoding, depending on platform
#
#                     +----------------------+               +--------------------+
#                     |                      |  Lo:30112     |                    |
#                     |                      +-------------->+  Front camera      |
#                     |                      |               |  decode/render     |
# +------------------>+                      |               +--------------------+
#    $1:$2            |  SCReAM receiver     |
# <-------------------+                      |               +--------------------+
#                     |                      |  Lo:30114     |                    |
#                     |                      +-------------->+  Rear  camera      |
#                     |                      |               |  decode/render     |
#                     +----------------------+               +--------------------+


# Start SCReAM receiver side
./scream/bin/scream_receiver $1 $2 $3 | tee ./Data/scream_$4.txt &

## /dev/video0
#gst-launch-1.0 udpsrc port=30112 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! vaapih264dec low-latency=true ! videoconvert ! waylandsink sync=true &
# gst-launch-1.0 udpsrc port=30112 ! application/x-rtp, media=video ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 ! queue ! filesink location=received_video_01.mp4 &
gst-launch udpsrc port=30112 caps ="application/x-rtp, media=(string)video, clock-rate=(int)90000, encoding-name=(string)MP4V-ES, profile-level-id=(string)6, config=(string)000001b006000001b59113000001000000012000c888800f528045a14103, payload=(int)96, ssrc=(guint)424830278, clock-base=(guint)2874253685, seqnum-base=(guint)43950" ! gstrtpjitterbuffer ! rtpmp4vdepay ! queue ! ffdec_mpeg4 ! ffmpegcolorspace ! mux_mp4 ! filesink location=myvideo.mp4

## /dev/video1
#gst-launch-1.0 udpsrc port=30114 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! vaapih264dec low-latency=true ! videoconvert ! ximagesink  sync=true &
gst-launch-1.0 udpsrc port=30114 ! application/x-rtp, media=video ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 ! queue ! filesink location=received_video.mp4 &

## /dev/video0
#gst-launch-1.0 udpsrc port=30112 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! waylandsink sync=true &
#gst-launch-1.0 udpsrc port=30112 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 low-latency=true ! videoconvert ! filesink location=./Video/output_video0.mp4
#gst-launch-1.0  udpsrc port=30112 ! v4l2src num-buffers=50 ! queue ! x264enc ! mp4mux ! filesink location=video.mp4
#gst-launch-1.0 udpsrc port=30000 ! application/x-rtp, media=(string)video ! rtph264pay name=pay ! queue ! avdec_h264 ! filesink location=received_video.mp4 &


## /dev/video1
#gst-launch-1.0 udpsrc port=30114 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! filesink location=./video1.mp4 ! ximagesink  sync=true &
#gst-launch-1.0 udpsrc port=30112 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 low-latency=true ! videoconvert ! filesink location=./Video/output_video1.mp4
