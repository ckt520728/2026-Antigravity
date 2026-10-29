/**
 * generate_pptx.js
 * Reproducible Node.js generator for:
 * "Rapid Alternation of Conscious & Suppressed Stimulus Representations in the Primate Brain" (Hesse et al. 2026)
 * Generates phase2/pptx/consciousness_rivalry_en.pptx with 12 slides and speaker notes citing fact IDs.
 * Zero external npm dependencies. Pure Node.js with built-in zlib.
 */

const fs = require("fs");
const path = require("path");
const zlib = require("zlib");

// --- ZIP UTILITY ---
class ZipBuilder {
  constructor() {
    this.files = [];
  }
  addFile(filePath, content) {
    const data = Buffer.isBuffer(content) ? content : Buffer.from(content, "utf8");
    const compressed = zlib.deflateRawSync(data);
    this.files.push({
      name: filePath.replace(/\\/g, "/"),
      data,
      compressed,
      crc: this.crc32(data),
      size: data.length,
      compSize: compressed.length
    });
  }
  crc32(buf) {
    let crc = 0 ^ (-1);
    for (let i = 0; i < buf.length; i++) {
      crc = (crc >>> 8) ^ this.table[(crc ^ buf[i]) & 0xFF];
    }
    return (crc ^ (-1)) >>> 0;
  }
  toBuffer() {
    let parts = [];
    let centralDir = [];
    let offset = 0;
    for (const f of this.files) {
      const nameBuf = Buffer.from(f.name, "utf8");
      const lh = Buffer.alloc(30);
      lh.writeUInt32LE(0x04034b50, 0);
      lh.writeUInt16LE(20, 4);
      lh.writeUInt16LE(0, 6);
      lh.writeUInt16LE(8, 8);
      lh.writeUInt16LE(0, 10);
      lh.writeUInt16LE(0, 12);
      lh.writeUInt32LE(f.crc, 14);
      lh.writeUInt32LE(f.compSize, 18);
      lh.writeUInt32LE(f.size, 22);
      lh.writeUInt16LE(nameBuf.length, 26);
      lh.writeUInt16LE(0, 28);
      parts.push(lh, nameBuf, f.compressed);

      const cd = Buffer.alloc(46);
      cd.writeUInt32LE(0x02014b50, 0);
      cd.writeUInt16LE(20, 4);
      cd.writeUInt16LE(20, 6);
      cd.writeUInt16LE(0, 8);
      cd.writeUInt16LE(8, 10);
      cd.writeUInt16LE(0, 12);
      cd.writeUInt16LE(0, 14);
      cd.writeUInt32LE(f.crc, 16);
      cd.writeUInt32LE(f.compSize, 20);
      cd.writeUInt32LE(f.size, 24);
      cd.writeUInt16LE(nameBuf.length, 28);
      cd.writeUInt16LE(0, 30);
      cd.writeUInt16LE(0, 32);
      cd.writeUInt16LE(0, 34);
      cd.writeUInt16LE(0, 36);
      cd.writeUInt32LE(0, 38);
      cd.writeUInt32LE(offset, 42);
      centralDir.push(cd, nameBuf);

      offset += lh.length + nameBuf.length + f.compressed.length;
    }
    const cdOffset = offset;
    let cdSize = 0;
    for (const b of centralDir) cdSize += b.length;

    const eocd = Buffer.alloc(22);
    eocd.writeUInt32LE(0x06054b50, 0);
    eocd.writeUInt16LE(0, 4);
    eocd.writeUInt16LE(0, 6);
    eocd.writeUInt16LE(this.files.length, 8);
    eocd.writeUInt16LE(this.files.length, 10);
    eocd.writeUInt32LE(cdSize, 12);
    eocd.writeUInt32LE(cdOffset, 16);
    eocd.writeUInt16LE(0, 20);

    return Buffer.concat([...parts, ...centralDir, eocd]);
  }
}
ZipBuilder.prototype.table = (() => {
  let c;
  const table = [];
  for (let n = 0; n < 256; n++) {
    c = n;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[n] = c;
  }
  return table;
})();

// --- SLIDE DATA DEFINITIONS ---
const slides = [
  {
    num: 1,
    category: "VISUAL NEUROSCIENCE & CONSCIOUSNESS",
    title: "Rapid Alternation of Conscious & Suppressed Stimulus Representations in the Primate Brain",
    subtitle: "Doris Tsao Lab (Oct 2026 bioRxiv preprint) &bull; Janis Hesse et al.",
    bullets: [
      "Key question: How does the primate brain represent sensory stimuli during visual suppression?",
      "Core discovery: Neural populations rapidly alternate (~15 Hz) between conscious and suppressed states.",
      "Authors: Hesse, Lanfranchi, McGrory, Shi, Engel, and Doris Y. Tsao (UC Berkeley, Caltech, Princeton, HHMI).",
      "Status: bioRxiv preprint, not yet peer reviewed (posted Oct 16, 2026; DOI: 10.64898/2026.10.15.759299)."
    ],
    footer: "bioRxiv preprint, not yet peer reviewed &bull; DOI 10.64898/2026.10.15.759299",
    notes: "Welcome audience. Presenting Doris Tsao's lab preprint posted October 16, 2026. Crucially emphasize: bioRxiv preprint, not yet peer reviewed. Cites F01, F02, F03, F05, F06."
  },
  {
    num: 2,
    category: "BACKGROUND & PUZZLE",
    title: "The 30-Year Mystery: Weak Modulation in IT Cortex",
    subtitle: "Why did neural correlates of consciousness seem so faint?",
    bullets: [
      "Binocular rivalry dissociates constant retinal input from shifting subjective conscious perception.",
      "Classical expectation: Inferotemporal (IT) face cells should fire strongly for conscious faces and fall silent for suppressed faces.",
      "Empirical paradox: Across 30 years of studies, time-averaged modulation was surprisingly weak (slope &approx; 0.23).",
      "Key scientific dilemma: Does the brain truly discard unseen images, or did time-averaging obscure fine dynamics?"
    ],
    footer: "Paradigm & Historical Background &bull; Time-Averaged Slope &approx; 0.23",
    notes: "Review binocular rivalry and flash suppression history (Logothetis, Sheinberg). Explain that past studies averaged over hundreds of milliseconds, revealing only a weak modulation slope of ~0.23. Cites F09, F27."
  },
  {
    num: 3,
    category: "EXPERIMENTAL PARADIGM",
    title: "Binocular Flash Suppression (BFS)",
    subtitle: "Deterministic perceptual suppression validated in humans at 82%",
    bullets: [
      "BFS paradigm: A variant of binocular rivalry giving millisecond-precision control over perceptual transitions.",
      "Trial sequence: Priming face presented to one eye (1&ndash;2 s), followed by a flashed face to the opposite eye.",
      "Perceptual takeover: The flashed stimulus reliably suppresses the prime (82% dominance validated in 14 humans).",
      "Visual display: Red-cyan stereoscopic anaglyph glasses at 7&deg; visual angle."
    ],
    footer: "Binocular Flash Suppression Paradigm &bull; Human Validation 82%",
    notes: "Detail BFS: prime for 1 or 2s, flash to other eye. Flash dominates in 82% of trials (t(13)=9.4). Eliminates motor report confounds. Cites F09, F11, F12, F13, F14, F25."
  },
  {
    num: 4,
    category: "ELECTROPHYSIOLOGY",
    title: "Massive Neuropixels Recording Across 4 Cortical Patches",
    subtitle: "High-density single-trial sampling in IT and Prefrontal Cortex",
    bullets: [
      "Subjects: 2 male rhesus macaques implanted with Neuropixels 1.0 NHP high-density probes.",
      "IT Face Patches: Middle lateral (ML, feature-based) and anterior medial (AM, identity-based) patches.",
      "Prefrontal Patches: Orbital (PO) and ventrolateral (PVL) prefrontal face patches.",
      "Data scale: 3,501 visual responsive units across sessions, including 661 prefrontal cortex neurons."
    ],
    footer: "2 Macaques &bull; 3,501 Visual Units &bull; Patches ML, AM, PO, PVL",
    notes: "Describe recordings: 2 monkeys, Neuropixels 1.0 NHP. Patches ML and AM in IT, PO and PVL in PFC. 3,501 visual units, 661 PFC units. Cites F15, F16, F17, F18, F19."
  },
  {
    num: 5,
    category: "ANALYTICAL FRAMEWORK",
    title: "No-Report Decoding with 10 ms Hidden Markov Models",
    subtitle: "Eliminating decision and motor confounds via statistical state modeling",
    bullets: [
      "No-report paradigm: Monkeys made no physical report; perceptual states were inferred directly from neural spikes.",
      "Fine temporal bins: Spikes binned in 10 ms sliding time windows (analysis bin, not state duration).",
      "Poisson LLR: Log-likelihood ratio compared single-trial activity to unconfounded single-stimulus templates.",
      "Decisive victory: 2-state Hidden Markov Model outperformed single-state static models in 19 out of 19 sessions."
    ],
    footer: "10 ms Poisson LLR + 2-State HMM &bull; 19/19 Sessions Outperform Single-State",
    notes: "Explain analytical approach: no-report removes motor confounds. 10 ms bin Poisson LLR and 2-state Poisson HMM. 2-state model won in 19/19 sessions. Cites F23, F29, F38."
  },
  {
    num: 6,
    category: "PRIMARY FINDING",
    title: "Populations Rapidly Alternate at ~15 Hz (~60 ms Dwell)",
    subtitle: "Conscious and suppressed representations trade places ~15 times per second",
    bullets: [
      "High-speed alternation: Populations trade between conscious (State 1) and suppressed (State 2) representations ~15 Hz.",
      "Dwell time: Average micro-epoch duration is ~60 ms (mean 67 ms, median 46&ndash;64 ms; State 1 = 64 ms, State 2 = 59 ms).",
      "Single-trial decoding: In State 1, 10-class conscious face decoding exceeds 61% (suppressed face is 4%; chance 10%).",
      "Orders of magnitude faster: 15 Hz alternation is >10x faster than conscious perceptual switching (~0.5 Hz)."
    ],
    footer: "Alternation &approx; 15 Hz &bull; Mean Dwell &approx; 67 ms &bull; Decoding > 61%",
    notes: "Highlight the core breakthrough: ~15 Hz alternation (~60 ms dwell time). State 1 decodes conscious face >61% vs 4% suppressed. Cites F28, F30, F31, F32, F36, F67."
  },
  {
    num: 7,
    category: "NEURAL CODING",
    title: "The Unseen Face Occupies the Full 50-D Face Space",
    subtitle: "Suppressed stimuli are not weak phantoms; they retain full-fidelity representation",
    bullets: [
      "Full geometric representation: During State 2 epochs, the suppressed face occupies the full 50-D feature face space.",
      "Robust firing rates: Overall mean firing rate in State 2 is slightly higher than in State 1.",
      "Same neural substrate: The exact same individual neurons alternate between representations (no separate sub-pools).",
      "Sensory persistence: High-level visual cortex faithfully encodes sensory reality regardless of subjective awareness."
    ],
    footer: "Same Neurons Switch &bull; Full 50-D Face Space &bull; Higher Firing Rate in State 2",
    notes: "Emphasize: the suppressed face is not lost or blurred. It occupies the full 50-D face space. Same neurons represent both faces. Firing rate in State 2 is slightly higher. Cites F41, F42, F53."
  },
  {
    num: 8,
    category: "QUANTITATIVE RIGOR",
    title: "Scientific Effect Size: 1.21 Tuning Gain Ratio",
    subtitle: "Distinguishing genuine effect size from statistical comparison p-values",
    bullets: [
      "Tuning gain ratio: Neurons exhibit a 1.21 gain elevation during conscious vs suppressed epochs (r = 0.90).",
      "The true effect size: The scientific magnitude is the 1.21 ratio (21% gain increase), NOT the p-value alone.",
      "Statistical context: p = 3 &times; 10^-40 reflects massive sample size and gain comparison precision, not raw magnitude.",
      "Single-cell modulation: The conscious percept modulates response gain rather than shifting receptive field tuning."
    ],
    footer: "Effect Size = 1.21 Gain Ratio (r = 0.90) &bull; p = 3x10^-40",
    notes: "Clarify quantitative metrics: 1.21 tuning gain ratio (r=0.90) is the effect size. Cite p = 3x10^-40 only in comparison context of conscious gain vs suppressed gain. Cites F39, F40."
  },
  {
    num: 9,
    category: "THEORETICAL RESOLUTION",
    title: "Time-Averaging Cancellation Resolves the 30-Year Mystery",
    subtitle: "Why past studies saw flat slopes: positive and negative epochs canceled out",
    bullets: [
      "Micro-epoch reality: Alternating 60 ms periods carry robust, opposite tuning (+21% gain vs -21% gain).",
      "Time-averaged artifact: Blending across 500&ndash;700 ms algebraically cancels the two signals into a flat 0.23 slope.",
      "Equalization proof: When micro-epoch gain is computationally equalized, residual correlation vanishes (r = -0.02).",
      "Methodological milestone: Unmasks the hidden dynamics that traditional time-averaging systematically erased."
    ],
    footer: "Cancellation Explains Weak Modulation &bull; Residual Correlation r = -0.02",
    notes: "Explain resolution: 15 Hz alternation of opposite gain signals cancels out when averaged over 500-700 ms, producing the flat 0.23 slope seen in earlier literature. Gain equalization leaves r = -0.02. Cites F27, F43."
  },
  {
    num: 10,
    category: "CORTICAL GENERALITY",
    title: "Widespread Scope: Qualitatively Similar Alternation in PFC",
    subtitle: "Temporal multiplexing extends into executive frontoparietal nodes",
    bullets: [
      "Prefrontal involvement: Both patch PO and PVL in prefrontal cortex display qualitatively similar ~15 Hz alternation.",
      "PFC reconstruction: Decoding fidelity in PFC is lower (priming EV < 80%, shape < 30%), reflecting abstract encoding.",
      "Weak inter-patch synchrony: ML-AM switching coordination is weak, indicating locally autonomous temporal dynamics.",
      "Cortical hypothesis: Authors propose temporal multiplexing may be a widespread, general principle of cortical processing."
    ],
    footer: "PFC Qualitatively Similar &bull; Weak ML-AM Coordination &bull; General Principle",
    notes: "Discuss cortical scope: PFC patches PO and PVL show similar ~15 Hz alternation. Reconstruction quality is lower in PFC. Authors suggest temporal multiplexing is a widespread cortical phenomenon. Cites F47, F48, F50, F52."
  },
  {
    num: 11,
    category: "SCIENTIFIC GUARDRAILS",
    title: "Critical Guardrails: What This Finding Does NOT Claim",
    subtitle: "Explicitly refuting overclaims and enforcing theoretical boundaries",
    bullets: [
      "Refuting 'Consciousness has a frame rate' (F57 contradicted): Tsao explicitly clarified they did NOT prove a frame rate.",
      "Subjective continuity: Population representation alternation does not mean conscious perception flickers or jumps.",
      "Theoretical attribution: The preprint does not cite or evaluate GNWT or IIT; links to ignition or phi are external interpretation.",
      "Frequency specificity: 15 Hz sits in low-beta band; it is distinctly NOT theta (4&ndash;8 Hz) or alpha (8&ndash;12 Hz)."
    ],
    footer: "No Frame Rate Claim &bull; Tsao Clarification &bull; Guardrails Enforced",
    notes: "Enforce guardrails: F57 ('consciousness has a frame rate') is contradicted and false. Tsao clarified they did not prove a frame rate. Paper does not cite GNWT/IIT. 15 Hz is not theta or alpha. Cites F55, F56, F57."
  },
  {
    num: 12,
    category: "SUMMARY & HORIZONS",
    title: "Summary & Open Scientific Frontiers",
    subtitle: "A dynamic new framework for understanding the stream of consciousness",
    bullets: [
      "Sensory retention: The primate brain multiplexes suppressed visual inputs alongside conscious percepts at ~15 Hz.",
      "The readout question: How do downstream executive circuits selectively route conscious micro-epochs into behavior?",
      "Switching driver: The biological trigger driving the ~60 ms alternation cycle remains unknown.",
      "Preprint reminder: bioRxiv preprint, not yet peer reviewed; conducted in 2 male macaques tested exclusively on faces."
    ],
    footer: "bioRxiv preprint, not yet peer reviewed &bull; Open Questions &bull; End of Deck",
    notes: "Conclude presentation: summarize 15 Hz multiplexing, open questions regarding readout and switching mechanism. Remind audience of preprint status, 2 monkeys, face stimuli only. Cites F01, F15, F54."
  }
];

// --- OPENXML TEMPLATES ---
function buildContentTypes() {
  let sldTypes = "";
  for (let i = 1; i <= slides.length; i++) {
    sldTypes += `  <Override PartName="/ppt/slides/slide${i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>\n`;
    sldTypes += `  <Override PartName="/ppt/notesSlides/notesSlide${i}.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.notesSlide+xml"/>\n`;
  }
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml" ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml" ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/theme/theme1.xml" ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
${sldTypes}</Types>`;
}

function buildRootRels() {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="ppt/presentation.xml"/>
</Relationships>`;
}

function buildPresentationRels() {
  let rels = `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdMaster1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="slideMasters/slideMaster1.xml"/>
`;
  for (let i = 1; i <= slides.length; i++) {
    rels += `  <Relationship Id="rIdSlide${i}" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="slides/slide${i}.xml"/>\n`;
  }
  rels += `</Relationships>`;
  return rels;
}

function buildPresentation() {
  let sldLst = "";
  for (let i = 1; i <= slides.length; i++) {
    sldLst += `    <p:sldId id="${255 + i}" r:id="rIdSlide${i}"/>\n`;
  }
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:presentation xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:sldMasterIdLst>
    <p:sldMasterId id="2147483648" r:id="rIdMaster1"/>
  </p:sldMasterIdLst>
  <p:sldIdLst>
${sldLst}  </p:sldIdLst>
  <p:sldSz cx="12192000" cy="6858000" type="screen16x9"/>
  <p:notesSz cx="6858000" cy="9144000"/>
</p:presentation>`;
}

function buildTheme() {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="Consciousness Dark Theme">
  <a:themeElements>
    <a:clrScheme name="Consciousness">
      <a:dk1><a:srgbClr val="0B0F19"/></a:dk1>
      <a:lt1><a:srgbClr val="F8FAFC"/></a:lt1>
      <a:dk2><a:srgbClr val="151D30"/></a:dk2>
      <a:lt2><a:srgbClr val="94A3B8"/></a:lt2>
      <a:accent1><a:srgbClr val="38BDF8"/></a:accent1>
      <a:accent2><a:srgbClr val="F43F5E"/></a:accent2>
      <a:accent3><a:srgbClr val="FBBF24"/></a:accent3>
      <a:accent4><a:srgbClr val="34D399"/></a:accent4>
      <a:accent5><a:srgbClr val="818CF8"/></a:accent5>
      <a:accent6><a:srgbClr val="C084FC"/></a:accent6>
      <a:hlink><a:srgbClr val="38BDF8"/></a:hlink>
      <a:folHlink><a:srgbClr val="818CF8"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Modern Sans">
      <a:majorFont><a:latin typeface="Segoe UI"/></a:majorFont>
      <a:minorFont><a:latin typeface="Segoe UI"/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Office">
      <a:fillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:fillStyleLst>
      <a:lnStyleLst><a:ln w="9525"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln></a:lnStyleLst>
      <a:effectStyleLst><a:effectStyle><a:effectLst/></a:effectStyle></a:effectStyleLst>
      <a:bgFillStyleLst><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:bgFillStyleLst>
    </a:fmtScheme>
  </a:themeElements>
</a:theme>`;
}

function buildSlideMaster() {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMap bg1="dk1" tx1="lt1" bg2="dk2" tx2="lt2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
  <p:sldLayoutIdLst>
    <p:sldLayoutId id="2147483649" r:id="rIdLayout1"/>
  </p:sldLayoutIdLst>
</p:sldMaster>`;
}

function buildSlideMasterRels() {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdLayout1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdTheme1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" Target="../theme/theme1.xml"/>
</Relationships>`;
}

function buildSlideLayout() {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" type="blank">
  <p:cSld name="Blank Layout">
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>`;
}

function buildSlideLayoutRels() {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdMaster" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" Target="../slideMasters/slideMaster1.xml"/>
</Relationships>`;
}

function escapeXml(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;").replace(/'/g, "&apos;");
}

function buildSlideXml(slide) {
  let bulletXml = "";
  slide.bullets.forEach((b, idx) => {
    bulletXml += `
      <a:p>
        <a:pPr marL="285750" indent="-285750">
          <a:buFont typeface="Arial"/>
          <a:buChar char="&bull;"/>
        </a:pPr>
        <a:r>
          <a:rPr lang="en-US" sz="2000" b="0">
            <a:solidFill><a:srgbClr val="CBD5E1"/></a:solidFill>
          </a:rPr>
          <a:t>${escapeXml(b)}</a:t>
        </a:r>
      </a:p>
      <a:p><a:pPr><a:spcBfr><a:spcPts val="1200"/></a:spcBfr></a:pPr></a:p>`;
  });

  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sld xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      
      <!-- Background Shape -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="SlideBg"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="0" y="0"/><a:ext cx="12192000" cy="6858000"/></a:xfrm>
          <a:prstGeom prst="rect"><a:avLst/></a:prstGeom>
          <a:solidFill><a:srgbClr val="0B0F19"/></a:solidFill>
        </p:spPr>
      </p:sp>

      <!-- Card Container Box -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="3" name="CardBox"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr>
        <p:spPr>
          <a:xfrm><a:off x="685800" y="548640"/><a:ext cx="10820400" cy="5760720"/></a:xfrm>
          <a:prstGeom prst="roundRect"><a:avLst><a:gd name="adj" fmla="val 2000"/></a:avLst></a:prstGeom>
          <a:solidFill><a:srgbClr val="151D30"/></a:solidFill>
          <a:ln w="12700"><a:solidFill><a:srgbClr val="23304C"/></a:solidFill></a:ln>
        </p:spPr>
      </p:sp>

      <!-- Category Label -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="4" name="Category"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="1097280" y="822960"/><a:ext cx="9997440" cy="400000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1300" b="1">
                <a:solidFill><a:srgbClr val="38BDF8"/></a:solidFill>
              </a:rPr>
              <a:t>${escapeXml(slide.category)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Main Title -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="5" name="Title"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="1097280" y="1234440"/><a:ext cx="9997440" cy="900000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="2600" b="1">
                <a:solidFill><a:srgbClr val="FFFFFF"/></a:solidFill>
              </a:rPr>
              <a:t>${escapeXml(slide.title)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Subtitle -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="6" name="Subtitle"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="1097280" y="2140000"/><a:ext cx="9997440" cy="400000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1500" i="1">
                <a:solidFill><a:srgbClr val="94A3B8"/></a:solidFill>
              </a:rPr>
              <a:t>${escapeXml(slide.subtitle)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

      <!-- Bullet Points -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="7" name="Bullets"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="1097280" y="2650000"/><a:ext cx="9997440" cy="3000000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
${bulletXml}
        </p:txBody>
      </p:sp>

      <!-- Footer Text -->
      <p:sp>
        <p:nvSpPr><p:cNvPr id="8" name="Footer"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="1097280" y="5780000"/><a:ext cx="9997440" cy="350000"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="0" tIns="0" rIns="0" bIns="0"/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1100">
                <a:solidFill><a:srgbClr val="64748B"/></a:solidFill>
              </a:rPr>
              <a:t>${escapeXml(slide.footer)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>

    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sld>`;
}

function buildSlideRels(idx) {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdLayout" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" Target="../slideLayouts/slideLayout1.xml"/>
  <Relationship Id="rIdNotes" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/notesSlide" Target="../notesSlides/notesSlide${idx}.xml"/>
</Relationships>`;
}

function buildNotesSlideXml(slide) {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:notes xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
      <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="NotesBody"/><p:cNvSpPr txBox="1"/><p:nvPr/></p:nvSpPr>
        <p:spPr><a:xfrm><a:off x="685800" y="685800"/><a:ext cx="5486400" cy="7772400"/></a:xfrm></p:spPr>
        <p:txBody>
          <a:bodyPr vert="horz" lIns="91440" tIns="45720" rIns="91440" bIns="45720"/>
          <a:p>
            <a:r>
              <a:rPr lang="en-US" sz="1200">
                <a:solidFill><a:srgbClr val="000000"/></a:solidFill>
              </a:rPr>
              <a:t>${escapeXml(slide.notes)}</a:t>
            </a:r>
          </a:p>
        </p:txBody>
      </p:sp>
    </p:spTree>
  </p:cSld>
  <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:notes>`;
}

function buildNotesSlideRels(idx) {
  return `<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rIdSlide" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" Target="../slides/slide${idx}.xml"/>
</Relationships>`;
}

// --- MAIN GENERATOR FUNCTION ---
function generatePresentation(outputPath) {
  console.log(`Generating presentation with ${slides.length} slides to ${outputPath}...`);
  const zip = new ZipBuilder();

  zip.addFile("[Content_Types].xml", buildContentTypes());
  zip.addFile("_rels/.rels", buildRootRels());
  zip.addFile("ppt/presentation.xml", buildPresentation());
  zip.addFile("ppt/_rels/presentation.xml.rels", buildPresentationRels());
  zip.addFile("ppt/theme/theme1.xml", buildTheme());
  zip.addFile("ppt/slideMasters/slideMaster1.xml", buildSlideMaster());
  zip.addFile("ppt/slideMasters/_rels/slideMaster1.xml.rels", buildSlideMasterRels());
  zip.addFile("ppt/slideLayouts/slideLayout1.xml", buildSlideLayout());
  zip.addFile("ppt/slideLayouts/_rels/slideLayout1.xml.rels", buildSlideLayoutRels());

  slides.forEach((s, idx) => {
    const slideIdx = idx + 1;
    zip.addFile(`ppt/slides/slide${slideIdx}.xml`, buildSlideXml(s));
    zip.addFile(`ppt/slides/_rels/slide${slideIdx}.xml.rels`, buildSlideRels(slideIdx));
    zip.addFile(`ppt/notesSlides/notesSlide${slideIdx}.xml`, buildNotesSlideXml(s));
    zip.addFile(`ppt/notesSlides/_rels/notesSlide${slideIdx}.xml.rels`, buildNotesSlideRels(slideIdx));
  });

  const buffer = zip.toBuffer();
  fs.mkdirSync(path.dirname(outputPath), { recursive: true });
  fs.writeFileSync(outputPath, buffer);
  console.log(`Successfully generated ${outputPath} (${buffer.length} bytes)!`);
}

// Execute
const outPptx = path.resolve(__dirname, "../consciousness_rivalry_en.pptx");
generatePresentation(outPptx);
