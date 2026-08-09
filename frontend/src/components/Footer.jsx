import "../styles/Footer.css";
import { FiCpu } from "react-icons/fi";

function Footer() {
  return (
    <footer className="footer">

      <h2>
    <FiCpu />
    {" "}
    AI Powered PCB Defect Detection
</h2>

      <p>
        Powered by <strong>YOLOv8</strong> • <strong>React</strong> • <strong>FastAPI</strong>
      </p>

      <p className="copyright">
        © 2026 CopyRight 
      </p>

    </footer>
  );
}

export default Footer;