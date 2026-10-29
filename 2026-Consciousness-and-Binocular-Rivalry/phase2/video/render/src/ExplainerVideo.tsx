import React from "react";
import {
  AbsoluteFill,
  Sequence,
  useCurrentFrame,
  interpolate,
  spring,
  useVideoConfig,
} from "remotion";

interface ShotDef {
  id: string;
  duration_s: number;
  unit: string;
  visual: string;
  narration_zh_tw: string;
  subtitles_zh_tw: string;
  fact_ids: string[];
}

const shots: ShotDef[] = [
  {
    id: "SHOT-01",
    duration_s: 15,
    unit: "視覺知覺與未解之謎",
    visual: "兩眼分別呈現不同影像的動畫演示。文字浮現：「你看見了什麼？」「雙眼競爭的知覺奧秘」。",
    narration_zh_tw: "你有沒有想過，當我們的兩隻眼睛，同時看到完全不一樣的畫面時，大腦會怎麼處理？",
    subtitles_zh_tw: "雙眼競爭（Binocular Rivalry）現象",
    fact_ids: [],
  },
  {
    id: "SHOT-02",
    duration_s: 15,
    unit: "視覺知覺與未解之謎",
    visual: "演示「雙眼閃光抑制（BFS）」實驗流程。前導刺激 1~2 秒，對側眼瞬間閃現新臉孔。",
    narration_zh_tw: "今年十月，加州大學柏克萊分校的曹穎實驗室，發表了一項突破性的預印本研究。他們採用了一種稱為雙眼閃光抑制的實驗範式。",
    subtitles_zh_tw: "雙眼閃光抑制（Binocular Flash Suppression, BFS）・82% 人類受試者驗證",
    fact_ids: ["F09", "F11", "F25"],
  },
  {
    id: "SHOT-03",
    duration_s: 15,
    unit: "視覺知覺與未解之謎",
    visual: "過去 30 年神經科學論文的時間平均放電折線圖，顯示幾乎平坦的弱調變（斜率僅約 0.23）。",
    narration_zh_tw: "過去三十年來，神經科學家一直想在高級視覺大腦皮質中，尋找意識的直接訊號。但平均起來看差距微乎其微。",
    subtitles_zh_tw: "過去時間平均研究中微弱的調變斜率（約 0.23）",
    fact_ids: ["F27"],
  },
  {
    id: "SHOT-04",
    duration_s: 20,
    unit: "實驗記錄與創新突破",
    visual: "3D 獼猴大腦模型透視圖。Neuropixels 1.0 探針穿刺進入下顳葉與前額葉皮質。斑塊 ML、AM、PO、PVL 依序點亮。",
    narration_zh_tw: "曹穎團隊使用新一代的神經探針技術，在兩隻恆河猴的大腦中展開高密度的單神經元記錄。",
    subtitles_zh_tw: "Neuropixels 1.0 NHP 探針・下顳葉 ML/AM 與前額葉 PO/PVL 斑塊・3501 個神經元",
    fact_ids: ["F15", "F16", "F17", "F18", "F19"],
  },
  {
    id: "SHOT-05",
    duration_s: 20,
    unit: "實驗記錄與創新突破",
    visual: "單次試驗神經放電點陣圖（Spike Raster）展示。每 10 毫秒時間窗（bin），透過 HMM 與 LLR 追蹤狀態軌跡。",
    narration_zh_tw: "這項研究的一大關鍵，在於徹底告別人為報告的干擾。透過每十毫秒一個時間窗的演算法與隱馬可夫模型，直接解碼大腦狀態。",
    subtitles_zh_tw: "無人為報告混淆範式・10 ms 時間窗 LLR + 雙狀態 HMM 演算法",
    fact_ids: ["F23", "F29"],
  },
  {
    id: "SHOT-06",
    duration_s: 20,
    unit: "實驗記錄與創新突破",
    visual: "單狀態模型與雙狀態模型對比圖表，十九個實驗場次全數標示綠色勾選標記（19/19）。",
    narration_zh_tw: "結果非常震撼。在全部十九個記錄場次中，假設大腦在兩種狀態間動態切換的雙狀態模型，一致勝過了單一靜態模型。",
    subtitles_zh_tw: "雙狀態模型於 19/19 場次全面勝過單狀態模型",
    fact_ids: ["F38"],
  },
  {
    id: "SHOT-07",
    duration_s: 25,
    unit: "核心發現：每秒十五次的時間多工",
    visual: "兩張臉孔在神經群體表徵中以約 15 Hz 快速閃爍輪替。停留時間約 60 ms（平均 67 ms）。",
    narration_zh_tw: "同一群神經元並沒有只鎖定你看見的那張臉。相反地，它們約每秒十五次，在看見的臉和被抑制的臉之間快速交替。",
    subtitles_zh_tw: "群體約每秒 15 次（約 15 Hz）交替・微時段停留時間平均約 60 ms（67 ms）・同一批神經元切換",
    fact_ids: ["F28", "F30", "F31", "F42", "F67"],
  },
  {
    id: "SHOT-08",
    duration_s: 20,
    unit: "核心發現：每秒十五次的時間多工",
    visual: "高維臉空間（Face Space）向量投影。顯示狀態一與狀態二佔據同樣寬廣的特徵幾何空間。",
    narration_zh_tw: "更驚人的是，那個被知覺壓制、主觀上完全看不見的刺激，在大腦裡絕不是微弱的殘影。在屬於它的微時段裡佔據完整臉空間。",
    subtitles_zh_tw: "被抑制刺激占據相同的完整臉空間・狀態二平均放電率略高",
    fact_ids: ["F41", "F53"],
  },
  {
    id: "SHOT-09",
    duration_s: 25,
    unit: "核心發現：每秒十五次的時間多工",
    visual: "15 Hz 正負相反的交替波形；時間平均後波形互相抵消拉平。",
    narration_zh_tw: "這完美解答了過去三十年的科學懸案。在看見的微時段中，調諧增益高出百分之二十一；時間平均把這兩個相反訊號抵消了。",
    subtitles_zh_tw: "狀態一調諧增益比 1.21（意識增益 vs 被抑制增益）・時間平均抵消解釋過去微弱調變",
    fact_ids: ["F39", "F40", "F43"],
  },
  {
    id: "SHOT-10",
    duration_s: 20,
    unit: "跨區現象、科學防線與總結",
    visual: "下顳葉與前額葉兩區各自展現高速交替現象。",
    narration_zh_tw: "這種每秒約十五次的高速交替，不僅發生在下顳葉的視覺斑塊，也同樣在負責高階決策的前額葉皮質中被觀察到。",
    subtitles_zh_tw: "下顳葉與前額葉皆展現高速交替・作者：可能是廣泛的皮質現象",
    fact_ids: ["F48", "F52"],
  },
  {
    id: "SHOT-11",
    duration_s: 20,
    unit: "跨區現象、科學防線與總結",
    visual: "大警語紅標：「科學邊界防線」。浮現曹穎教授的澄清引述：「我們並未證明意識有影格率」。",
    narration_zh_tw: "但我們必須非常謹慎。這項發現絕不等於意識有影格率。曹穎教授本人也特別澄清，他們並沒有證明意識有影格率。",
    subtitles_zh_tw: "嚴禁過度宣稱「意識有影格率」・作者澄清：未證明意識有影格率（初步）",
    fact_ids: ["F56"],
  },
  {
    id: "SHOT-12",
    duration_s: 25,
    unit: "跨區現象、科學防線與總結",
    visual: "論文標題卡：'Rapid alternation of conscious and suppressed stimulus representations in the primate brain'。醒目金色字體標註預印本警語。",
    narration_zh_tw: "這篇來自柏克萊與加州理工團隊的重要論文，目前為 bioRxiv 預印本、尚未經同儕審查。謝謝您的收看！",
    subtitles_zh_tw: "bioRxiv 預印本、尚未經同儕審查・感謝收看",
    fact_ids: ["F01", "F02", "F03", "F05", "F06"],
  },
];

export const ExplainerVideo: React.FC = () => {
  let accumulatedFrames = 0;

  return (
    <AbsoluteFill style={{ backgroundColor: "#070b14", color: "#f8fafc", fontFamily: "Noto Sans TC, sans-serif" }}>
      {shots.map((shot, index) => {
        const shotFrames = shot.duration_s * 30;
        const fromFrame = accumulatedFrames;
        accumulatedFrames += shotFrames;

        return (
          <Sequence key={shot.id} from={fromFrame} durationInFrames={shotFrames}>
            <ShotCard shot={shot} />
          </Sequence>
        );
      })}

      {/* Top Banner (Persistent) */}
      <div
        style={{
          position: "absolute",
          top: 32,
          left: 48,
          right: 48,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          borderBottom: "1px solid rgba(255,255,255,0.15)",
          paddingBottom: 16,
        }}
      >
        <span style={{ fontSize: 24, fontWeight: 700, color: "#38bdf8", letterSpacing: 1 }}>
          雙眼閃光抑制與意識時間多工 (Hesse et al. 2026)
        </span>
        <span
          style={{
            fontSize: 20,
            fontWeight: 600,
            background: "rgba(251, 191, 36, 0.2)",
            color: "#fbbf24",
            border: "1px solid #fbbf24",
            padding: "4px 16px",
            borderRadius: 9999,
          }}
        >
          bioRxiv 預印本、尚未經同儕審查
        </span>
      </div>
    </AbsoluteFill>
  );
};

const ShotCard: React.FC<{ shot: ShotDef }> = ({ shot }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const opacity = interpolate(frame, [0, 15], [0, 1], {
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        opacity,
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "120px 80px 100px",
      }}
    >
      {/* Unit Tag */}
      <div
        style={{
          fontSize: 26,
          fontWeight: 700,
          color: "#38bdf8",
          textTransform: "uppercase",
          letterSpacing: 2,
          marginBottom: 16,
        }}
      >
        {shot.unit} &bull; {shot.id}
      </div>

      {/* Visual Description Panel */}
      <div
        style={{
          background: "#131c31",
          border: "2px solid #243456",
          borderRadius: 24,
          padding: "48px 56px",
          width: "100%",
          maxWidth: 1400,
          boxShadow: "0 25px 60px rgba(0,0,0,0.5)",
          textAlign: "center",
        }}
      >
        <div style={{ fontSize: 44, fontWeight: 800, color: "#ffffff", lineHeight: 1.4, marginBottom: 28 }}>
          {shot.visual}
        </div>
        <div
          style={{
            fontSize: 32,
            color: "#94a3b8",
            lineHeight: 1.6,
            background: "rgba(0,0,0,0.3)",
            padding: "20px 32px",
            borderRadius: 16,
            borderLeft: "6px solid #38bdf8",
            textAlign: "left",
          }}
        >
          &ldquo;{shot.narration_zh_tw}&rdquo;
        </div>
      </div>

      {/* Subtitles Bar at Bottom */}
      <div
        style={{
          position: "absolute",
          bottom: 40,
          left: 80,
          right: 80,
          textAlign: "center",
          background: "rgba(3, 7, 18, 0.85)",
          border: "1px solid #1e293b",
          padding: "16px 24px",
          borderRadius: 12,
        }}
      >
        <span style={{ fontSize: 30, fontWeight: 700, color: "#f8fafc" }}>
          {shot.subtitles_zh_tw}
        </span>
      </div>
    </AbsoluteFill>
  );
};
