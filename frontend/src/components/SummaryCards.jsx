import "./SummaryCards.css";

function SummaryCards({ result }) {
    

    if (!result) return null;

    return (
    <div className="summary-container">

      <div className="summary-card">
        <h3>Total Defects</h3>
        <p>{result.total_detections}</p>
      </div>

      <div className="summary-card">
        <h3>Status</h3>
        <p>Completed ✅</p>
      </div>

      <div className="summary-card">
        <h3>Model</h3>
        <p>YOLOv8</p>
      </div>

      <div className="summary-card">
        <h3>Image</h3>
        <p>{result.filename}</p>
      </div>

    </div>
  );
}

export default SummaryCards;