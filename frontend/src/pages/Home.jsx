import Navbar from "../components/Navbar";
import UploadCard from "../components/UploadCard";

function Home() {
  return (
    <>
      <Navbar />

      <div
        style={{
          textAlign: "center",
          marginTop: "50px",
        }}
      >
        <h2>Welcome to AI Powered PCB Defect Detection</h2>
        <UploadCard />
      </div>
    </>
  );
}

export default Home;