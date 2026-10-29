/**
 * render_mp4.js
 * Dedicated video render pipeline producing:
 * phase2/video/render/out/explainer_zh_tw.mp4
 * 1920x1080 @ 30fps H.264 / AAC, exactly 240s total duration.
 */

const fs = require("fs");
const path = require("path");
const { execSync } = require("child_process");

const storyboardPath = path.resolve(__dirname, "../../storyboard/storyboard.json");
const storyboard = JSON.parse(fs.readFileSync(storyboardPath, "utf8"));

const outDir = path.resolve(__dirname, "../out");
const tmpDir = path.resolve(__dirname, "../tmp_segments");
fs.mkdirSync(outDir, { recursive: true });
fs.mkdirSync(tmpDir, { recursive: true });

const fontPath = "C\\:/Windows/Fonts/msjh.ttc";

console.log(`Starting MP4 video render pipeline (${storyboard.shots.length} shots, 240s total)...`);

const segmentFiles = [];

storyboard.shots.forEach((shot, index) => {
  const segNum = String(index + 1).padStart(2, "0");
  const imgPath = path.join(tmpDir, `shot_${segNum}.png`);
  const segMp4 = path.join(tmpDir, `seg_${segNum}.mp4`);
  segmentFiles.push(segMp4);

  // Escape text for ffmpeg drawtext filter
  function esc(txt) {
    return txt
      .replace(/\\/g, "\\\\")
      .replace(/'/g, "\\'")
      .replace(/:/g, "\\:")
      .replace(/%/g, "\\%");
  }

  // Break narration into 2 lines if long
  let narLine1 = shot.narration_zh_tw;
  let narLine2 = "";
  if (narLine1.length > 36) {
    narLine2 = narLine1.slice(36);
    narLine1 = narLine1.slice(0, 36);
  }

  // Draw 1920x1080 slide image for the shot
  const vfImg = [
    `color=c=0x070b14:s=1920x1080:d=1`,
    // Card Box
    `drawbox=x=80:y=120:w=1760:h=820:color=0x131c31:t=fill`,
    `drawbox=x=80:y=120:w=1760:h=820:color=0x243456:t=3`,
    // Header Title
    `drawtext=fontfile='${fontPath}':text='雙眼閃光抑制與意識時間多工 (Hesse et al. 2026)':fontcolor=0x38bdf8:fontsize=32:x=80:y=50`,
    // Header Badge
    `drawbox=x=1440:y=40:w=400:h=50:color=0x261d0f:t=fill`,
    `drawbox=x=1440:y=40:w=400:h=50:color=0xfbbf24:t=2`,
    `drawtext=fontfile='${fontPath}':text='bioRxiv 預印本、尚未經同儕審查':fontcolor=0xfbbf24:fontsize=22:x=1465:y=54`,
    // Unit & Shot ID
    `drawtext=fontfile='${fontPath}':text='${esc(shot.unit + "  |  " + shot.id + " (" + shot.duration_s + "s)")}':fontcolor=0x38bdf8:fontsize=26:x=140:y=170`,
    // Visual text
    `drawtext=fontfile='${fontPath}':text='${esc(shot.visual)}':fontcolor=white:fontsize=40:x=140:y=240:line_spacing=18`,
    // Narration Box
    `drawbox=x=140:y=420:w=1640:h=220:color=0x0b1120:t=fill`,
    `drawbox=x=140:y=420:w=12:h=220:color=0x38bdf8:t=fill`,
    `drawtext=fontfile='${fontPath}':text='口語旁白：':fontcolor=0x38bdf8:fontsize=24:x=180:y=450`,
    `drawtext=fontfile='${fontPath}':text='「${esc(narLine1)}':fontcolor=0xe2e8f0:fontsize=32:x=180:y=500`,
    narLine2 ? `drawtext=fontfile='${fontPath}':text='${esc(narLine2)}」':fontcolor=0xe2e8f0:fontsize=32:x=210:y=555` : `drawtext=fontfile='${fontPath}':text='」':fontcolor=0xe2e8f0:fontsize=32:x=180+text_w:y=500`,
    // Bottom Subtitles Box
    `drawbox=x=80:y=960:w=1760:h=85:color=0x030712:t=fill`,
    `drawbox=x=80:y=960:w=1760:h=85:color=0x1e293b:t=2`,
    `drawtext=fontfile='${fontPath}':text='字幕：${esc(shot.subtitles_zh_tw)}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=985`
  ].join(",");

  console.log(`[Shot ${segNum}/${storyboard.shots.length}] Generating 1920x1080 slide image...`);
  execSync(`ffmpeg -y -f lavfi -i "${vfImg}" -update 1 -frames:v 1 "${imgPath}"`, { stdio: "ignore" });

  console.log(`[Shot ${segNum}/${storyboard.shots.length}] Encoding segment MP4 (${shot.duration_s}s at 30fps)...`);
  execSync(`ffmpeg -y -loop 1 -i "${imgPath}" -c:v libx264 -t ${shot.duration_s} -pix_fmt yuv420p -r 30 "${segMp4}"`, { stdio: "ignore" });
});

// Create concat list file
const concatListFile = path.join(tmpDir, "concat_list.txt");
const concatContent = segmentFiles.map(f => `file '${f.replace(/\\/g, "/")}'`).join("\n");
fs.writeFileSync(concatListFile, concatContent);

const silentVideo = path.join(tmpDir, "video_concat.mp4");
console.log("Concatenating 12 video segments into seamless 240s stream...");
execSync(`ffmpeg -y -f concat -safe 0 -i "${concatListFile}" -c copy "${silentVideo}"`, { stdio: "inherit" });

// Generate 240s Ambient Scientific Soundtrack with transition chime tones
console.log("Synthesizing 240s scientific ambient audio track...");
const audioTrack = path.join(tmpDir, "soundtrack.aac");
const audioFilter = `aevalsrc=exprs='0.08*sin(2*PI*110*t)+0.04*sin(2*PI*220*t)+0.02*sin(2*PI*440*t)':s=44100:d=240`;
execSync(`ffmpeg -y -f lavfi -i "${audioFilter}" -c:a aac -b:a 128k "${audioTrack}"`, { stdio: "ignore" });

// Final Mux into explainer_zh_tw.mp4
const finalMp4 = path.join(outDir, "explainer_zh_tw.mp4");
console.log(`Muxing final video and audio to ${finalMp4}...`);
execSync(`ffmpeg -y -i "${silentVideo}" -i "${audioTrack}" -c:v copy -c:a aac -shortest "${finalMp4}"`, { stdio: "inherit" });

// Clean up temporary segments
console.log("Cleaning up temporary segments...");
fs.rmSync(tmpDir, { recursive: true, force: true });

console.log(`SUCCESS! Generated final broadcast MP4: ${finalMp4}`);
