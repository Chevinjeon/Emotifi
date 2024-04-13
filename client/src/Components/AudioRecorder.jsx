import { useState, useRef } from "react";
import './AudioRecorder.css';
import { IoMdReturnLeft } from "react-icons/io";
const AudioRecorder = () => {

    const mimeType = 'audio/webm'
    const [permission, setPermission] = useState(false);
    const [stream, setStream] = useState(null);

    const [recordingStatus, setRecordingStatus] = useState(false);
    const [audioChunks, setAudioChunks] =useState([])
    const [audio, setAudio] = useState(null)


    const mediaRecorder = useRef(null)

    const getMicrophonePermission = async () => {
        if ("MediaRecorder" in window) {
            try {
                const streamData = await navigator.mediaDevices.getUserMedia({
                    audio: true,
                    video: false,
                });
                setPermission(true);
                setStream(streamData);
            } catch (err) {
                alert(err.message);
            }
        } else {
            alert("The MediaRecorder API is not supported in your browser.");
        }
    };

    const startRecording = async () => {
        setRecordingStatus(true)

        const media = new MediaRecorder(stream, { type: mimeType });

        mediaRecorder.current = media

        mediaRecorder.current.start()

        let recordedAudio = []
        mediaRecorder.current.ondataavailable = (event) => {
            if (typeof event.data === "undefined") return;
            if (event.data.size === 0) return;
            recordedAudio.push(event.data)
        }
        setAudioChunks(recordedAudio)
    }

    const stopRecording = () => {
        setRecordingStatus(false)

        mediaRecorder.current.stop()
        mediaRecorder.current.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: mimeType });
            const audioUrl = URL.createObjectURL(audioBlob)
            setAudio(audioUrl);
            setAudioChunks([])
        }
    }
    
    return (
        <div>
            <h2>Audio Recorder</h2>
            <main>
                <div className="audio-controls">
                    {!permission ? (
                        <button onClick={getMicrophonePermission} type="button">
                            Get Microphone
                        </button>
                    ): null}
                    {permission && recordingStatus === false ? (
                        <button onClick={startRecording} type="button">
                            Start recording
                        </button>
                    ): null}
                    {recordingStatus === true ? (
                        <button onClick={stopRecording} type="button">
                            Stop Recording
                        </button>
                    ): null}
                    {audio ? (
                        <div className='audio-container'>
                            <audio src={audio} controls></audio>
                            <a download href={audio}>
                                Download Recording
                            </a>
                        </div>
                    ): null}
                </div>
            </main>
        </div>
    );
};
export default AudioRecorder;