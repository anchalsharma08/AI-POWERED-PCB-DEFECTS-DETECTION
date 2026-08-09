import jsPDF from "jspdf";
import "./DownloadReportButton.css";
import autoTable from "jspdf-autotable";

function DownloadReportButton({ analysis, detections, imageUrl }) {

    const loadImage = (url) => {
    return new Promise((resolve, reject) => {
        const img = new Image();

        img.crossOrigin = "Anonymous";

        img.onload = () => resolve(img);

        img.onerror = reject;

        img.src = url;
    });
};

    const downloadPDF = async () => {
        const doc = new jsPDF();
        let currentY = 20;

        const checkPageBreak = (requiredSpace = 20) => {

        const pageHeight = doc.internal.pageSize.getHeight();

        if (currentY + requiredSpace > pageHeight - 20) {

        doc.addPage();

        currentY = 20;

        }

        };

        doc.setFont("helvetica", "bold");

        doc.setFontSize(24);

        doc.text("PCB INSPECTION REPORT", 20, currentY);
        currentY += 15;

        doc.setDrawColor(37, 99, 235);

        doc.setLineWidth(0.6);

        doc.line(
        20,
        currentY - 10,
        190,
        currentY - 10
        );

        doc.setFontSize(12);

        doc.setFont("helvetica", "normal");

        doc.text(
        "AI Powered PCB Defect Detection System",
        20,
        currentY
        );
        currentY += 8;

        doc.text(
        "Model : YOLOv8",
        20,
        currentY
        );

        currentY += 8;

        doc.text(
        `Report ID : ${analysis.inspection_id}`,
        20,
        currentY
        );

        currentY += 8;

        doc.text(
        `Generated : ${analysis.timestamp}`,
        20,
        currentY
        );

        currentY += 15;

        doc.setFont("helvetica", "bold");

        doc.setFontSize(18);

        checkPageBreak(40);

        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);

        doc.text("INSPECTION SUMMARY", 20, currentY);

        currentY += 10;

        // doc.setFont("helvetica", "normal");

        // doc.setFontSize(12);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(12);

        doc.text(
        `Total Defects : ${analysis.total_defects}`,
        20,
        currentY
        );

        currentY += 8;

        doc.text(
        `Highest Confidence : ${analysis.highest_confidence}%`,
        20,
        currentY
        );

        currentY += 8;

        doc.text(
        `Average Confidence : ${analysis.average_confidence}%`,
        20,
        currentY
        );

        currentY += 8;

        doc.text(
        `Inspection Status : ${analysis.inspection_status}`,
        20,
        currentY
        );

        currentY += 15;

         doc.setDrawColor(200);

        doc.line(20, 150, 190, 150);

        checkPageBreak(50);

        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);

        doc.text("AI RECOMMENDATION", 20, currentY);
        currentY += 10;

        doc.setDrawColor(200);

        doc.line(20, 150, 190, 150);

        doc.setFont("helvetica", "normal");
        doc.setFontSize(12);

        const recommendationLines = doc.splitTextToSize(
            analysis.recommendation,
            170
        );

        doc.text(
            recommendationLines,
            20,
            currentY
        );

        currentY += recommendationLines.length * 7 + 12;
        
        checkPageBreak(60);

currentY += 8;
        doc.setFont("helvetica", "bold");
        doc.setFontSize(18);

        doc.text("INSPECTION OBSERVATIONS", 20, currentY);
        currentY += 10;

        doc.setFont("helvetica", "normal");
        doc.setFontSize(12);

        analysis.observations.forEach((item) => {

        doc.text(`• ${item}`, 25, currentY);

        currentY += 8;

        });
        currentY += 10;

       
        

        checkPageBreak(100);
         doc.setFont("helvetica", "bold");
        doc.setFontSize(18);
        
         doc.text("DETECTION TABLE", 20, currentY);
        currentY += 10;
    autoTable(doc, {

    startY: currentY,

    head: [["#", "Defect", "Confidence"]],

    body: detections.map((item, index) => [

        index + 1,

        item.type,

        `${(item.confidence * 100).toFixed(2)}%`

    ]),

    theme: "grid",

    headStyles: {

        fillColor: [37, 99, 235],

        textColor: 255,

        halign: "center"

    },

    bodyStyles: {

        halign: "center"

    }

    });
         
        currentY = doc.lastAutoTable.finalY + 15;


        checkPageBreak(120);

doc.setDrawColor(180);

doc.line(20, currentY, 190, currentY);

currentY += 8;

doc.setFont("helvetica", "bold");
doc.setFontSize(18);

doc.text(
    "ANNOTATED PCB RESULT",
    20,
    currentY
);

        currentY += 12;
        
        doc.setFont("helvetica", "normal");
doc.setFontSize(12);

doc.text(
    "Inspection Model : YOLOv8",
    20,
    currentY
);

currentY += 8;

doc.text(
    "Confidence Threshold : 25%",
    20,
    currentY
);

currentY += 8;

doc.text(
    "Image Resolution : 640 × 640",
    20,
    currentY
);

        currentY += 12;
        
        // =======================================
// LOAD & INSERT ANNOTATED PCB IMAGE
// =======================================

try {

    checkPageBreak(140);

    const img = await loadImage(imageUrl);

    const canvas = document.createElement("canvas");

    const ctx = canvas.getContext("2d");

    canvas.width = img.width;
    canvas.height = img.height;

    ctx.drawImage(img, 0, 0);

    const imgData = canvas.toDataURL("image/jpeg");

    const maxWidth = 170;

    const maxHeight = 110;

    const ratio = Math.min(
        maxWidth / img.width,
        maxHeight / img.height
    );

    const imgWidth = img.width * ratio;

    const imgHeight = img.height * ratio;

    const x = (210 - imgWidth) / 2;

    doc.addImage(
        imgData,
        "JPEG",
        x,
        currentY,
        imgWidth,
        imgHeight
    );

    currentY += imgHeight + 8;

    doc.setFont("helvetica", "italic");
    doc.setFontSize(11);

    doc.text(
        "Figure 1 : YOLOv8 PCB Defect Detection Result",
        105,
        currentY,
        {
            align: "center"
        }
    );

    currentY += 15;

}
catch (error) {

    console.error(error);

    doc.setTextColor(220,0,0);

    doc.text(
        "Unable to load annotated PCB image.",
        20,
        currentY
    );

    currentY += 10;

    doc.setTextColor(0,0,0);

}



        checkPageBreak(60);
        doc.setDrawColor(180);

doc.line(
    20,
    currentY,
    190,
    currentY
);

currentY += 10;

doc.setFont("helvetica", "bold");
doc.setFontSize(14);

doc.text(
    "Generated By",
    20,
    currentY
);

currentY += 8;

doc.setFont("helvetica", "normal");
doc.setFontSize(12);

doc.text(
    "AI Powered PCB Defect Detection System",
    20,
    currentY
);

currentY += 8;

doc.text(
    "Model : YOLOv8",
    20,
    currentY
);

currentY += 8;

doc.text(
    `Report ID : ${analysis.inspection_id}`,
    20,
    currentY
);

currentY += 8;

doc.text(
    `Generated : ${analysis.timestamp}`,
    20,
    currentY
);

currentY += 12;

doc.setFontSize(10);

doc.text(
    "© 2026 AI Powered PCB Defect Detection System",
    20,
    currentY
);

        doc.save(
            `PCB_Inspection_Report_${analysis.inspection_id}.pdf`);
    };

    return (

        <button
            onClick={downloadPDF}
            className="download-report-btn"
        >

            Download Inspection Report

        </button>

    );

}

export default DownloadReportButton;