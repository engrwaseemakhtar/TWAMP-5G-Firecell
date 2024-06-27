# AWS-TWAMP-scream
Installation Manual

# Group Gmail Access
user: miuncsndev@gmail.com

pass: 3e@reCSN


# AWS Access (https://aws.amazon.com/)
user: miuncsndev@gmail.com

pass: 3e@reCSN

---
## Creating New EC2 Instance on AWS

### Step 1: Sign in to AWS Console

Navigate to the [AWS Management Console](https://aws.amazon.com/console/) and sign in using your credentials.

### Step 2: Launch EC2 Instance

1. Click on the **Services** dropdown menu and select **EC2** under the Compute section.
2. Click on **Launch Instance** to start the EC2 instance creation process.

### Step 3: Choose an Amazon Machine Image (AMI)

1. Select an AMI based on your requirements, such as Amazon Linux, Ubuntu, or Windows Server.
2. Click **Select** to proceed.

### Step 4: Choose an Instance Type

1. Choose an instance type based on your workload needs.
2. Click **Next: Configure Instance Details**.

### Step 5: Configure Instance Details

1. Set configurations like network settings, subnet, IAM role, etc., as per your requirements.
2. Click **Next: Add Storage**.

### Step 6: Add Storage

1. Define the storage requirements for your EC2 instance.
2. Click **Next: Add Tags**.

### Step 7: Add Tags

1. (Optional) Add tags to your instance for better organization and management.
2. Click **Next: Configure Security Group**.

### Step 8: Configure Security Group

1. Create a new security group or select an existing one.
2. Configure inbound and outbound rules to control traffic to and from your instance.
3. Click **Review and Launch**.

### Step 9: Review and Launch

1. Review your instance configuration.
2. Click **Launch**.

### Step 10: Select an Existing Key Pair or Create a New Key Pair

1. Choose an existing key pair or create a new one.
2. Check the acknowledgment box and click **Launch Instances**.

### Step 11: Access Your EC2 Instance

1. Once the instance is launched, you can access it via SSH (for Linux instances) or RDP (for Windows instances) using the key pair you selected or created.
2. Use the instance's public IP address or public DNS to connect.

---
# FileZilla Access
To access the EC2 via FileZilla, please download the software and utilize the following credentials.

Download [FileZilla](https://filezilla-project.org/)

User Name
```
ubuntu
```

Password (Key) [miunkey.pem](https://github.com/MIUN-CSN/AWS-TWAMP-scream/blob/main/muinkey.pem)
```
https://github.com/MIUN-CSN/AWS-TWAMP-scream/blob/main/muinkey.pem
```

---
# TWAMP Test 
Responder (Should use Private IP of the current server:Port) 
```
sudo python3 twampy.py responder 172.31.19.82:862
```
Sender (Should user Public IP of the server:Port)
```
sudo python3 twampy.py sender -i 100 -c 100 16.170.229.66:862
```

---
# SCReAM

SCReAM (Self-Clocked Rate Adaptation for Multimedia) is a congestion control algorithm devised mainly for Video. Congestion control for WebRTC media is currently being standardized in the IETF RMCAT WG, the scope of the working group is to define requirements for congestion control and also to standardize a few candidate solutions. SCReAM is a congestion control candidate solution for WebRTC developed at Ericsson Research and optimized for good performance in wireless access.

The algorithm is an IETF experimental standard [1], a Sigcomm paper [2] and [3] explains the rationale behind the design of the algorithm in more detail. Because SCReAM as most other congestion control algorithms are continously improved over time, the current implementation available here has deviated from what is described in the papers and IETF RFC. The most important new development is addition of L4S support. In addition the algorithm has been modified to become more stable.

As mentioned above, SCReAM was originally devised for WebRTC but did not make it into being incorporated into that platform. Instead, SCReAM has found use as congestion control for remote controlled vehicles, cloud gaming demos and benchmarking of 5G networks with and without L4S support.

```
sudo apt update
```
```
sudo apt install g++
```
```
sudo apt install git
```
```
sudo apt install make
```
```
sudo apt  install cmake
```
```
git clone https://github.com/EricssonResearch/scream.git
```
```
cmake .
```
```
make
```
---
### Installing G Streammer

```
sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad gstreamer1.0-plugins-ugly gstreamer1.0-libav gstreamer1.0-tools gstreamer1.0-x gstreamer1.0-alsa gstreamer1.0-gl gstreamer1.0-gtk3 gstreamer1.0-qt5 gstreamer1.0-pulseaudio
```

#### Optional (G Streammer Knowledge)

GStreamer is a powerful open-source multimedia framework that provides a pipeline-based architecture for constructing media processing applications. It offers a wide range of plugins for handling various multimedia tasks, including playback, recording, encoding, decoding, and streaming.

In the context of SCReAM (Self-Clocked Rate Adaptation for Multimedia), GStreamer is utilized as the streaming library for managing media streams, particularly for real-time communication scenarios like video conferencing and VoIP (Voice over Internet Protocol).

A typical GStreamer pipeline for SCReAM might involve several elements, each responsible for different tasks in the streaming process. Here's a simplified example of a GStreamer pipeline for SCReAM:

```bash
gst-launch-1.0 -v \
  videotestsrc ! videoconvert ! x264enc ! h264parse ! rtph264pay ! \
  queue ! screamtx ! \
  udpsink host=127.0.0.1 port=5004
```

Let's break down this pipeline:

1. **videotestsrc**: This element generates test video frames. In a real-world scenario, this would be replaced with a source element that captures video frames from a camera or a video file.

2. **videoconvert**: Converts the video format to the required format for encoding.

3. **x264enc**: Encodes the video frames using the x264 codec. Other codecs can also be used depending on requirements.

4. **h264parse**: Parses the H.264 encoded data to make it compatible with the RTP payload format.

5. **rtph264pay**: Prepares the H.264 encoded data for RTP transmission.

6. **queue**: Buffers the encoded video frames to ensure smooth transmission.

7. **screamtx**: SCReAM element responsible for congestion control and rate adaptation. It adjusts the transmission rate based on network conditions to optimize quality and minimize latency.

8. **udpsink**: Sends the RTP packets over UDP to the specified host and port. In a real-world scenario, this would typically be replaced with elements for transmitting over a network.

This pipeline represents a basic setup for streaming video using SCReAM with GStreamer. Depending on specific requirements and configurations, additional elements and parameters may be added or modified to optimize performance and functionality.

It's worth noting that GStreamer offers extensive flexibility and customization options, allowing developers to tailor the pipeline according to their unique streaming requirements and integrate additional features as needed.

---
# SCReAM Bandwidth Test (https://github.com/EricssonResearch/scream/blob/master/SCReAM-BW-test-tool.pptx)

How to run it?

Receiver side:>./bin/scream-bw-test-rx <sender side IP> <port>

Sender side:>./bin/scream-bw-test-tx <receiver side IP> <port>


---
# SCReAM Multicameras Test (https://github.com/EricssonResearch/scream/tree/master/multicam)

Receiver : 
```
gst-launch-1.0 udpsrc port=30000 ! application/x-rtp, media=(string)video ! rtph264pay name=pay ! queue ! avdec_h264 ! filesink location=received_video.mp4 &
```
Receiver Test: 

" Start SCReAM receiver side"
```
./scream/bin/scream_receiver $1 $2 $3 | tee ./Data/scream_$4.txt &
```

"## /dev/video0"
```
gst-launch-1.0 udpsrc port=30112 ! application/x-rtp,media=video,clock-rate=90000,encoding-name=H264 ! rtpjitterbuffer latency=50 ! rtph264depay ! h264parse ! avdec_h264 ! videoconvert ! filesink location=/path/to/output_video.mp4
```


Sender : 

```
gst-launch-1.0 rtpbin name=rtpbin multifilesrc location=$MEDIA location=$MEDIA loop=true stop-index=-1 ! qtdemux name=demux ! queue ! h264parse ! avdec_h264 ! queue ! x264enc tune=zerolatency bitrate=1000000 ! queue max-size-buffers=2 ! rtph264pay mtu=1300 ! udpsink host=127.0.0.1 port=30000 &
```

---
# ufw firewall

```
sudo ufw default allow incoming
```

```
sudo ufw default allow outgoing
```




