import { useRef } from "react";
import Webcam from "react-webcam";
import "./WebcamCapture.css";

function WebcamCapture({ onCapture,  onClose  }) {

    const webcamRef = useRef(null);

    const captureImage = () => {

    const imageSrc = webcamRef.current.getScreenshot();

        onCapture(imageSrc);
         onClose();

};

    return (

        <div className="webcam-container">

            <h2>Capture PCB using Webcam</h2>

            <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                className="webcam"
            />

            <button
    className="capture-btn"
    onClick={captureImage}
>
    📷 Capture PCB
</button>

        </div>

    );

}

export default WebcamCapture;