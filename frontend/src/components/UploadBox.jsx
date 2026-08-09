import "./UploadBox.css";
import { FiUploadCloud } from "react-icons/fi";

function UploadBox({ file, onFileChange }) {
  return (
    <div className="upload-box">

      <label htmlFor="pcb-upload" className="upload-label">

        <div className="upload-icon"><FiUploadCloud/></div>

        <h3>Upload PCB Image</h3>

        <p>Click to Browse PCB Image</p>

        <small>Supports JPG • JPEG • PNG</small>

        <div className="file-name">
          {file ? `✅ ${file.name}` : "No file selected"}
        </div>

      </label>

      <input
        id="pcb-upload"
        type="file"
        accept=".jpg,.jpeg,.png"
        onChange={onFileChange}
      />

    </div>
  );
}

export default UploadBox;