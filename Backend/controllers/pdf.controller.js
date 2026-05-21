import { spawn } from "child_process";
import path from "path";
import fs from "fs";
import { fileURLToPath } from "url";
import { dirname } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const uploadsDir = path.join(__dirname, "../uploads");
const scriptsDir = path.join(__dirname, "../DataScrapingScripts");

function deleteFile(filePath) {
  fs.unlink(filePath, (err) => {
    if (err) console.error("Error deleting PDF file:", err);
    else console.log("PDF file deleted successfully");
  });
}

function runScraper(scriptName, pdfPath, res) {
  const scriptPath = path.join(scriptsDir, scriptName);
  const pythonProcess = spawn("python", [scriptPath, pdfPath]);

  let responded = false;
  let output = "";

  pythonProcess.stdout.on("data", (data) => {
    output += data.toString();
  });

  pythonProcess.stderr.on("data", (data) => {
    console.error(`stderr: ${data}`);
  });

  pythonProcess.on("close", (code) => {
    deleteFile(pdfPath);
    if (responded) return;
    responded = true;

    if (code !== 0) {
      return res.status(500).send("Error processing PDF");
    }
    try {
      const extractedData = JSON.parse(output);
      res.json(extractedData);
    } catch (error) {
      console.error("Error parsing JSON from Python script:", error);
      res.status(500).send("Error processing PDF");
    }
  });
}

export const heartScraper = (req, res) => {
  const pdfPath = path.join(uploadsDir, req.file.filename);
  runScraper("scrapHeart.py", pdfPath, res);
};

export const diabetesScraper = (req, res) => {
  const pdfPath = path.join(uploadsDir, req.file.filename);
  runScraper("scrapDiabetes.py", pdfPath, res);
};
