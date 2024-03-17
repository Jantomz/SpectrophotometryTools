const express = require("express");
const fs = require("fs");
const https = require("https");
const cors = require("cors");
const multer = require("multer");

const app = express();
const port = 3000;

// Specify the path to the text file
app.use(cors());

app.get("/api", (req, res) => {
  const filePath = req.query.filePath;

  // Read the file asynchronously
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error(err);
      res.status(500).send("Error reading file");
      return;
    }

    // Split the file content into an array of lines
    const lines = data.split("\n");

    const numOfSets = lines[0].split(",").length / 2;
    console.log(`Number of Datasets: ${numOfSets}`);

    let sets = [];

    for (const line of lines) {
      sets.push([]);
    }

    // Print each line
    for (let i = 0; i < numOfSets; i++) {
      lines.forEach((line, index) => {
        sets[index][i * 2] = line.split(",")[i * 2];
        sets[index][i * 2 + 1] = line.split(",")[i * 2 + 1];
      });
    }

    const properSets = [];
    for (let i = 0; i < numOfSets * 2; i++) {
      properSets.push([]);
    }

    for (let i = 0; i < numOfSets; i++) {
      for (let j = 0; j < sets.length; j++) {
        properSets[i * 2].push(sets[j][i * 2]);
        properSets[i * 2 + 1].push(sets[j][i * 2 + 1]);
      }
    }

    for (let i = 0; i < properSets.length; i++) {
      for (let j = 0; j < properSets[i].length; j++) {
        properSets[i][j] = Number(properSets[i][j]);
      }
    }

    res.send(properSets);
  });
});

// Set up multer middleware to handle file uploads
const upload = multer({ dest: "uploads/" });

app.post("/api", upload.single("file"), (req, res) => {
  const filePath = req.file.path;

  // Read the file asynchronously
  fs.readFile(filePath, "utf8", (err, data) => {
    if (err) {
      console.error(err);
      res.status(500).send("Error reading file");
      return;
    }

    // Split the file content into an array of lines
    const lines = data.split("\n");

    // Check if the first line is text and not numbers
    if (isNaN(lines[0].split(",")[0])) {
      lines.shift(); // Remove the first line
    }

    if (lines[lines.length - 1].trim() === "") {
      lines.pop(); // Remove the last line
    }

    const numOfSets = lines[0].split(",").length / 2;
    console.log(`Number of Datasets: ${numOfSets}`);

    let sets = [];

    for (const line of lines) {
      sets.push([]);
    }

    // Print each line
    for (let i = 0; i < numOfSets; i++) {
      lines.forEach((line, index) => {
        sets[index][i * 2] = line.split(",")[i * 2];
        sets[index][i * 2 + 1] = line.split(",")[i * 2 + 1];
      });
    }

    const properSets = [];
    for (let i = 0; i < numOfSets * 2; i++) {
      properSets.push([]);
    }

    for (let i = 0; i < numOfSets; i++) {
      for (let j = 0; j < sets.length; j++) {
        properSets[i * 2].push(sets[j][i * 2]);
        properSets[i * 2 + 1].push(sets[j][i * 2 + 1]);
      }
    }

    for (let i = 0; i < properSets.length; i++) {
      for (let j = 0; j < properSets[i].length; j++) {
        properSets[i][j] = Number(properSets[i][j]);
      }
    }

    res.send(properSets);
  });
});

app.listen(port, () => {
  console.log(`Server listening at http://localhost:${port}`);
});
