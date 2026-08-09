import "./DetectionTable.css";

function DetectionTable({ detections }) {
  if (!detections || detections.length === 0) {
    return (
      <div className="empty-state">
        <h3>No Defects Detected ✅</h3>
        <p>Upload a PCB image to begin inspection.</p>
      </div>
    );
  }

  return (
    <div className="table-container">

      <h2 className="table-title">
        Detected Defects
          </h2>
          <div className="tabel-wrapper">

      <table className="detection-table">

        <thead>
          <tr>
            <th>#</th>
            <th>Detected Defect</th>
            <th>Confidence Score</th>
          </tr>
        </thead>

        <tbody>

          {detections.map((item, index) => {

            const confidence = item.confidence * 100;

            let badgeClass = "low";

            if (confidence >= 80) {
              badgeClass = "high";
            }

            else if (confidence >= 50) {
              badgeClass = "medium";
            }

            return (

              <tr key={index}>

                <td>{index + 1}</td>

                <td>{item.type}</td>

                <td>

                  <span className={`confidence ${badgeClass}`}>

                    {confidence.toFixed(2)}%

                  </span>

                </td>

              </tr>

            );

          })}

        </tbody>

            </table>
        </div>

    </div>
  );
}

export default DetectionTable;