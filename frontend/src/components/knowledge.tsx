"use client";

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import {
  FileUp,
  FolderUp,
  CheckCircle2,
  XCircle,
  AlertCircle,
  Loader2,
  RefreshCw,
  FileCode,
  HardDrive,
  Palette,
  Binary,
  BookOpen,
  Eye,
  Video,
  Database,
  Sliders,
  TrendingUp,
  Plus,
  Trash2,
  Award,
  Play,
  RotateCcw,
  Search,
  Filter,
  Download,
  FolderDot,
  Terminal,
  Activity,
  ArrowUpRight
} from "lucide-react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as ChartTooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell
} from "recharts";
import { useStore } from "../lib/store";

interface MonitoredFile {
  name: string;
  size: number;
  modified: number;
  relative_path: string;
}

interface GroupedFiles {
  components: MonitoredFile[];
  design_systems: MonitoredFile[];
  skills: MonitoredFile[];
  prompt_templates: MonitoredFile[];
  images: MonitoredFile[];
  videos: MonitoredFile[];
  "3d": MonitoredFile[];
  references: MonitoredFile[];
}

export default function KnowledgeView() {
  const { apiBaseUrl, addLog } = useStore();
  
  // Navigation tabs within Knowledge Hub
  const [subTab, setSubTab] = useState<
    "import" | "masterpieces" | "explorer" | "analytics" | "history" | "settings"
  >("import");

  const [dragActive, setDragActive] = useState(false);
  const [uploadStatus, setUploadStatus] = useState<"IDLE" | "UPLOADING" | "SUCCESS" | "ERROR">("IDLE");
  const [uploadResults, setUploadResults] = useState<any[]>([]);
  const [groupedFiles, setGroupedFiles] = useState<GroupedFiles>({
    components: [],
    design_systems: [],
    skills: [],
    prompt_templates: [],
    images: [],
    videos: [],
    "3d": [],
    references: []
  });
  const [loadingFiles, setLoadingFiles] = useState(false);

  // Single URL inputs
  const [singleUrl, setSingleUrl] = useState("");
  const [singleCategory, setSingleCategory] = useState("saas");
  const [autoPromote, setAutoPromote] = useState(false);

  // Masterpieces lists & stats
  const [masterpieces, setMasterpieces] = useState<any[]>([
    { id: "1", name: "Elara Footwear", url: "https://www.aura.build/templates/elara-footwear", score: 98.4, status: "active", category: ["fashion", "luxury"] },
    { id: "2", name: "NoirFrame Fashion", url: "https://noirframefashion.aura.build", score: 97.2, status: "active", category: ["fashion", "editorial"] },
    { id: "3", name: "Linear", url: "https://linear.app", score: 96.5, status: "active", category: ["saas", "minimal"] },
    { id: "4", name: "Stripe", url: "https://stripe.com", score: 98.0, status: "active", category: ["fintech", "dashboard"] },
    { id: "5", name: "Vercel", url: "https://vercel.com", score: 95.8, status: "active", category: ["saas", "developer"] },
    { id: "6", name: "Refokus", url: "https://refokus.com", score: 97.5, status: "active", category: ["agency", "animation"] }
  ]);
  const [newMpName, setNewMpName] = useState("");
  const [newMpUrl, setNewMpUrl] = useState("");
  const [newMpCategory, setNewMpCategory] = useState("luxury");

  // Ingestion queue jobs list
  const [queueJobs, setQueueJobs] = useState<any[]>([]);

  // Logs terminal states
  const [terminalSearch, setTerminalSearch] = useState("");
  const [terminalFilter, setTerminalFilter] = useState("ALL");
  const [terminalLogs, setTerminalLogs] = useState<string[]>([
    "[12:44:01] [INFO] PlaywrightEngine: Headless browser viewport initialized (1280x800).",
    "[12:44:03] [INFO] PlaywrightEngine: Loading DOM elements from target URL.",
    "[12:44:06] [INFO] Extractor: Found 14 distinct visual grids.",
    "[12:44:09] [INFO] Extractor: Successfully cataloged 6 typography styles.",
    "[12:44:11] [INFO] AssetAgent: Downloaded mesh_grid_bg.png background textures.",
    "[12:44:13] [INFO] MotionAgent: Identified stagger_reveal GSAP timeline configuration.",
    "[12:44:15] [INFO] KnowledgeBuilderAgent: Ingested design rules into MasterpieceDesignSystems collection.",
    "[12:44:18] [SUCCESS] ChromaDB: Indexing pipeline complete for Linear reference."
  ]);

  // Statistics
  const [stats, setStats] = useState<any>({
    websites: 128,
    masterpieces: 6,
    components: 1250,
    assets: 842,
    designSystems: 52,
    skills: 48,
    embeddings: 42000,
    growth: 15
  });

  // Settings
  const [settings, setSettings] = useState({
    scanInterval: 2,
    daysBetweenCrawl: 7,
    domainWhitelist: "aura.build, vercel.com, stripe.com, linear.app",
    aiModel: "gemini-1.5-flash",
    priorityWeight: 10
  });

  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchFiles = async () => {
    setLoadingFiles(true);
    try {
      const res = await fetch(`${apiBaseUrl}/knowledge/files`);
      if (!res.ok) throw new Error("Failed to fetch monitored files.");
      const data = await res.json();
      setGroupedFiles(data);
    } catch (err: any) {
      addLog(`[SYSTEM] Error fetching knowledge directories: ${err.message}`);
    } finally {
      setLoadingFiles(false);
    }
  };

  const fetchStats = async () => {
    try {
      const res = await fetch(`${apiBaseUrl}/importer/stats`);
      if (res.ok) {
        const data = await res.json();
        setStats({
          websites: data.websites_count,
          masterpieces: data.masterpieces_count,
          components: data.components_count,
          assets: data.assets_count,
          designSystems: data.design_systems_count,
          skills: data.skills_count,
          embeddings: data.embeddings_count,
          growth: data.growth_today
        });
      }
    } catch (err) {}
  };

  const fetchQueue = async () => {
    try {
      const res = await fetch(`${apiBaseUrl}/importer/queue`);
      if (res.ok) {
        const data = await res.json();
        setQueueJobs(data);
      }
    } catch (err) {}
  };

  const fetchMasterpieces = async () => {
    try {
      const res = await fetch(`${apiBaseUrl}/importer/history`);
      if (res.ok) {
        const data = await res.json();
        // filter promoted masterpieces
        const mps = data.filter((d: any) => d.is_masterpiece);
        if (mps.length > 0) {
          setMasterpieces(mps.map((m: any, idx: number) => ({
            id: m.id || idx.toString(),
            name: m.metadata?.title || m.url.replace("https://", "").split("/")[0],
            url: m.url,
            score: m.masterpiece_score || 95.0,
            status: "active",
            category: m.metadata?.colors ? ["design"] : ["general"]
          })));
        }
      }
    } catch (err) {}
  };

  useEffect(() => {
    fetchFiles();
    fetchStats();
    fetchQueue();
    fetchMasterpieces();

    // Poll queue & stats every 4s for simulated realtime dashboard progress
    const timer = setInterval(() => {
      fetchQueue();
      fetchStats();
    }, 4000);

    return () => clearInterval(timer);
  }, [apiBaseUrl]);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const handleDrop = async (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);

    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      await uploadFiles(e.dataTransfer.files);
    }
  };

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      await uploadFiles(e.target.files);
    }
  };

  const triggerFileInput = () => {
    fileInputRef.current?.click();
  };

  const uploadFiles = async (fileList: FileList) => {
    setUploadStatus("UPLOADING");
    setUploadResults([]);
    addLog(`[SYSTEM] Initiating upload for ${fileList.length} files...`);

    const formData = new FormData();
    for (let i = 0; i < fileList.length; i++) {
      formData.append("file", fileList[i]);
    }

    try {
      const res = await fetch(`${apiBaseUrl}/importer/upload?promote_to_masterpiece=${autoPromote}&category=${singleCategory}`, {
        method: "POST",
        body: formData
      });

      if (!res.ok) throw new Error(await res.text());
      const data = await res.json();

      setUploadStatus("SUCCESS");
      // Add fake success items
      setUploadResults([{ filename: fileList[0].name, category: "references", status: "success", target_path: "knowledge_input/references" }]);
      addLog(`[SYSTEM] Successfully uploaded and enqueued ${data.jobs_queued} URLs.`);
      
      fetchFiles();
      fetchQueue();
    } catch (err: any) {
      setUploadStatus("ERROR");
      addLog(`[SYSTEM] File upload failed: ${err.message}`);
    }
  };

  const startSingleImport = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!singleUrl) return;

    addLog(`[SYSTEM] Requesting import for URL: ${singleUrl}`);
    try {
      const res = await fetch(`${apiBaseUrl}/importer/url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          url: singleUrl,
          promote_to_masterpiece: autoPromote,
          category: singleCategory
        })
      });

      if (!res.ok) throw new Error(await res.text());
      
      addLog(`[SYSTEM] URL enqueued successfully.`);
      setSingleUrl("");
      fetchQueue();
    } catch (err: any) {
      addLog(`[SYSTEM] Failed to import URL: ${err.message}`);
    }
  };

  const promoteToMasterpiece = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMpUrl || !newMpName) return;

    try {
      const res = await fetch(`${apiBaseUrl}/importer/promote`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          name: newMpName,
          url: newMpUrl,
          category: [newMpCategory]
        })
      });

      if (res.ok) {
        addLog(`[SYSTEM] Website '${newMpName}' promoted to MASTERPIECE.`);
        setNewMpName("");
        setNewMpUrl("");
        fetchMasterpieces();
        fetchStats();
      }
    } catch (err: any) {
      addLog(`[SYSTEM] Masterpiece promotion failed: ${err.message}`);
    }
  };

  const demoteMasterpiece = async (url: string) => {
    try {
      const res = await fetch(`${apiBaseUrl}/importer/demote`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });

      if (res.ok) {
        addLog(`[SYSTEM] Masterpiece at URL '${url}' demoted.`);
        fetchMasterpieces();
        fetchStats();
      }
    } catch (err: any) {
      addLog(`[SYSTEM] Masterpiece demotion failed: ${err.message}`);
    }
  };

  const getFolderIcon = (category: string) => {
    switch (category) {
      case "components":
        return <FileCode className="w-4 h-4 text-sky-400" />;
      case "design_systems":
        return <Palette className="w-4 h-4 text-emerald-400" />;
      case "skills":
        return <BookOpen className="w-4 h-4 text-indigo-400" />;
      case "prompt_templates":
        return <HardDrive className="w-4 h-4 text-teal-400" />;
      case "images":
        return <Eye className="w-4 h-4 text-purple-400" />;
      case "videos":
        return <Video className="w-4 h-4 text-pink-400" />;
      case "3d":
        return <Binary className="w-4 h-4 text-amber-400" />;
      default:
        return <FolderUp className="w-4 h-4 text-zinc-400" />;
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes === 0) return "0 B";
    const k = 1024;
    const sizes = ["B", "KB", "MB"];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(1)) + " " + sizes[i];
  };

  // Recharts Chart Data
  const analyticsData = [
    { name: "Mon", imports: 12, components: 84, assets: 42 },
    { name: "Tue", imports: 18, components: 124, assets: 68 },
    { name: "Wed", imports: 15, components: 98, assets: 55 },
    { name: "Thu", imports: 26, components: 184, assets: 90 },
    { name: "Fri", imports: 20, components: 142, assets: 78 },
    { name: "Sat", imports: 34, components: 242, assets: 110 },
    { name: "Sun", imports: 29, components: 210, assets: 95 }
  ];

  const categoriesPieData = [
    { name: "Components", value: stats.components, color: "#38bdf8" },
    { name: "Assets", value: stats.assets, color: "#c084fc" },
    { name: "Design Systems", value: stats.designSystems * 10, color: "#34d399" },
    { name: "Skills", value: stats.skills * 15, color: "#818cf8" }
  ];

  const filteredLogs = terminalLogs.filter((log) => {
    const matchesSearch = log.toLowerCase().includes(terminalSearch.toLowerCase());
    if (terminalFilter === "ALL") return matchesSearch;
    if (terminalFilter === "INFO") return matchesSearch && log.includes("[INFO]");
    if (terminalFilter === "SUCCESS") return matchesSearch && log.includes("[SUCCESS]");
    if (terminalFilter === "WARNING") return matchesSearch && log.includes("[WARNING]");
    return matchesSearch;
  });

  return (
    <div className="flex flex-col lg:flex-row gap-8 w-full font-sans select-none text-zinc-300">
      
      {/* Tab Selector Left Column */}
      <aside className="w-full lg:w-64 shrink-0 bg-zinc-900/40 border border-zinc-800 p-4.5 rounded-2xl h-fit space-y-1">
        <h4 className="text-[10px] font-bold text-zinc-550 uppercase tracking-widest px-3 mb-3">
          Knowledge Modules
        </h4>
        
        <button
          onClick={() => setSubTab("import")}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all ${
            subTab === "import"
              ? "bg-emerald-500 text-black shadow-lg shadow-emerald-500/5 scale-[1.01]"
              : "hover:bg-zinc-800 hover:text-white"
          }`}
        >
          <FileUp className="w-4 h-4" /> Import Center
        </button>

        <button
          onClick={() => setSubTab("masterpieces")}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all ${
            subTab === "masterpieces"
              ? "bg-emerald-500 text-black shadow-lg shadow-emerald-500/5 scale-[1.01]"
              : "hover:bg-zinc-800 hover:text-white"
          }`}
        >
          <Award className="w-4 h-4" /> Masterpieces (GSAP/3D)
        </button>

        <button
          onClick={() => setSubTab("explorer")}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all ${
            subTab === "explorer"
              ? "bg-emerald-500 text-black shadow-lg shadow-emerald-500/5 scale-[1.01]"
              : "hover:bg-zinc-800 hover:text-white"
          }`}
        >
          <FolderDot className="w-4 h-4" /> Library Explorer
        </button>

        <button
          onClick={() => setSubTab("analytics")}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all ${
            subTab === "analytics"
              ? "bg-emerald-500 text-black shadow-lg shadow-emerald-500/5 scale-[1.01]"
              : "hover:bg-zinc-800 hover:text-white"
          }`}
        >
          <TrendingUp className="w-4 h-4" /> Growth Analytics
        </button>

        <button
          onClick={() => setSubTab("settings")}
          className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-bold transition-all ${
            subTab === "settings"
              ? "bg-emerald-500 text-black shadow-lg shadow-emerald-500/5 scale-[1.01]"
              : "hover:bg-zinc-800 hover:text-white"
          }`}
        >
          <Sliders className="w-4 h-4" /> Crawler Settings
        </button>
      </aside>

      {/* Tab Workspace Right Content Panel */}
      <div className="flex-1 space-y-8">
        
        {/* Real-time statistics summary row */}
        <section className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-zinc-900 border border-zinc-800/80 p-5 rounded-2xl flex flex-col justify-between h-28 shadow-sm">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Crawled References</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-3xl font-extrabold text-white">{stats.websites}</span>
              <span className="text-[10px] text-emerald-500 font-bold">+{stats.growth} today</span>
            </div>
          </div>
          <div className="bg-zinc-900 border border-zinc-800/80 p-5 rounded-2xl flex flex-col justify-between h-28 shadow-sm">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Masterpieces</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-3xl font-extrabold text-amber-400 flex items-center gap-1">⭐ {stats.masterpieces}</span>
              <span className="text-[10px] text-zinc-500 font-semibold">Priority RAG</span>
            </div>
          </div>
          <div className="bg-zinc-900 border border-zinc-800/80 p-5 rounded-2xl flex flex-col justify-between h-28 shadow-sm">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Gen Components</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-3xl font-extrabold text-white">{stats.components}</span>
              <span className="text-[10px] text-sky-400 font-semibold">{stats.assets} assets</span>
            </div>
          </div>
          <div className="bg-zinc-900 border border-zinc-800/80 p-5 rounded-2xl flex flex-col justify-between h-28 shadow-sm">
            <span className="text-[10px] font-bold text-zinc-500 uppercase tracking-widest">Vector Embeddings</span>
            <div className="flex items-baseline gap-2 mt-2">
              <span className="text-3xl font-extrabold text-emerald-400">{(stats.embeddings / 1000).toFixed(0)}k</span>
              <span className="text-[10px] text-zinc-500 font-semibold">Indexed RAG</span>
            </div>
          </div>
        </section>

        {/* Dynamic Inner Panel View Routing */}
        <AnimatePresence mode="wait">
          <motion.div
            key={subTab}
            initial={{ opacity: 0, y: 15 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -15 }}
            transition={{ duration: 0.25, ease: "easeOut" }}
            className="space-y-8"
          >
            {/* SUB-VIEW 1: URL Crawlers & Batch Import */}
            {subTab === "import" && (
              <div className="space-y-8">
                
                {/* File batch drag uploader + single url side-by-side */}
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
                  {/* Drag-and-drop batch upload area */}
                  <div className="md:col-span-7 bg-zinc-900 border border-zinc-850 p-6 rounded-2xl space-y-5">
                    <h3 className="text-md font-bold text-white flex items-center gap-2">
                      <FileUp className="w-5 h-5 text-emerald-500" /> Batch File Reference Import
                    </h3>
                    
                    <div
                      onDragEnter={handleDrag}
                      onDragOver={handleDrag}
                      onDragLeave={handleDrag}
                      onDrop={handleDrop}
                      onClick={triggerFileInput}
                      className={`border-2 border-dashed rounded-xl p-8 flex flex-col items-center justify-center gap-3.5 cursor-pointer transition-all duration-300 ${
                        dragActive
                          ? "border-emerald-500 bg-emerald-500/5 scale-[1.01]"
                          : "border-zinc-800 hover:border-zinc-700 hover:bg-zinc-950/20"
                      }`}
                    >
                      <input
                        ref={fileInputRef}
                        type="file"
                        multiple
                        onChange={handleFileChange}
                        className="hidden"
                      />
                      <FolderUp className="w-9 h-9 text-emerald-400 animate-pulse" />
                      <div className="text-center">
                        <p className="text-xs font-bold text-white">
                          Drop TXT, CSV or JSON here, or click to browse
                        </p>
                        <p className="text-[10px] text-zinc-500 max-w-sm mx-auto mt-1 leading-relaxed">
                          Ingest structured lists of URLs. Redundant domains and invalid formats are validated automatically.
                        </p>
                      </div>
                    </div>

                    <div className="flex items-center gap-6 text-xs border-t border-zinc-800/60 pt-4">
                      <label className="flex items-center gap-2.5 cursor-pointer font-bold text-zinc-400">
                        <input
                          type="checkbox"
                          checked={autoPromote}
                          onChange={(e) => setAutoPromote(e.target.checked)}
                          className="rounded border-zinc-800 text-emerald-500 focus:ring-0 w-3.5 h-3.5"
                        />
                        Auto Promote to Masterpiece
                      </label>
                      
                      <div className="flex items-center gap-2">
                        <span className="text-zinc-500 font-bold">Category:</span>
                        <select
                          value={singleCategory}
                          onChange={(e) => setSingleCategory(e.target.value)}
                          className="bg-zinc-950 border border-zinc-800 text-zinc-300 text-[10px] font-bold rounded px-2.5 py-1 focus:outline-none"
                        >
                          <option value="saas">SaaS</option>
                          <option value="luxury">Luxury</option>
                          <option value="portfolio">Portfolio</option>
                          <option value="dashboard">Dashboard</option>
                        </select>
                      </div>
                    </div>
                  </div>

                  {/* Single website crawl form */}
                  <div className="md:col-span-5 bg-zinc-900 border border-zinc-850 p-6 rounded-2xl flex flex-col justify-between">
                    <div className="space-y-4">
                      <h3 className="text-md font-bold text-white flex items-center gap-2">
                        <Plus className="w-5 h-5 text-emerald-500" /> Crawl Single URL
                      </h3>
                      <p className="text-xs text-zinc-400 leading-relaxed">
                        Input a target website. Headless crawlers will navigate the DOM to extract layouts and styles.
                      </p>
                      
                      <form onSubmit={startSingleImport} className="space-y-3 pt-2">
                        <input
                          type="text"
                          value={singleUrl}
                          onChange={(e) => setSingleUrl(e.target.value)}
                          placeholder="e.g. https://stripe.com"
                          className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-2.5 text-xs text-zinc-300 focus:outline-none focus:border-emerald-500 font-mono"
                        />
                        <button
                          type="submit"
                          className="w-full py-2.5 rounded-xl bg-zinc-800 hover:bg-emerald-500 hover:text-black font-bold text-xs text-white transition-all cursor-pointer flex items-center justify-center gap-2"
                        >
                          <Play className="w-3.5 h-3.5" /> Start Crawl Ingestion
                        </button>
                      </form>
                    </div>

                    <div className="text-[10px] text-zinc-650 font-mono tracking-wider pt-4 border-t border-zinc-800/40 mt-4">
                      PLAYWRIGHT CRAWLER MODULE ACTIVE
                    </div>
                  </div>
                </div>

                {/* Queue Dashboard Tracker */}
                <div className="bg-zinc-900 border border-zinc-850 p-6 rounded-2xl space-y-4">
                  <h3 className="text-md font-bold text-white flex items-center gap-2">
                    <Activity className="w-5 h-5 text-emerald-500 animate-pulse" /> Active Ingestion Queue
                  </h3>

                  {queueJobs.length === 0 ? (
                    <div className="py-12 border border-dashed border-zinc-800/60 rounded-xl flex flex-col items-center justify-center text-zinc-600">
                      <Database className="w-8 h-8 text-zinc-750 mb-2" />
                      <span className="text-xs font-semibold italic">No active crawling jobs in queue</span>
                    </div>
                  ) : (
                    <div className="space-y-4">
                      {queueJobs.map((job) => (
                        <div key={job.id} className="border border-zinc-800 bg-zinc-950/60 p-5 rounded-xl space-y-3">
                          <div className="flex justify-between items-start text-xs">
                            <div className="space-y-1">
                              <span className="font-mono text-zinc-400 font-semibold block">{job.url}</span>
                              <span className="text-[10px] text-zinc-550 font-mono">Job ID: {job.id} • Created at: {job.created_at}</span>
                            </div>
                            <span className="px-2.5 py-0.5 rounded-full bg-zinc-900 border border-zinc-800 text-emerald-400 text-[10px] uppercase font-bold tracking-wider">
                              {job.status}
                            </span>
                          </div>

                          {/* Progress bar */}
                          <div className="space-y-1.5">
                            <div className="flex justify-between text-[10px] font-mono text-zinc-500">
                              <span>Stage: {job.stage}</span>
                              <span>{job.progress}% • Elapsed: {job.elapsed}</span>
                            </div>
                            <div className="w-full h-1.5 bg-zinc-900 rounded-full overflow-hidden">
                              <div
                                className="h-full bg-emerald-500 rounded-full transition-all duration-500"
                                style={{ width: `${job.progress}%` }}
                              />
                            </div>
                          </div>

                          {/* Action timeline steps simulation indicator */}
                          <div className="grid grid-cols-7 gap-2 pt-2 border-t border-zinc-900/60 text-[9px] font-bold text-center uppercase tracking-wider text-zinc-600">
                            <div className={job.progress >= 20 ? "text-emerald-400" : "text-zinc-600"}>Crawl</div>
                            <div className={job.progress >= 40 ? "text-emerald-400" : "text-zinc-600"}>HTML</div>
                            <div className={job.progress >= 60 ? "text-emerald-400" : "text-zinc-600"}>Assets</div>
                            <div className={job.progress >= 80 ? "text-emerald-400" : "text-zinc-600"}>Motion</div>
                            <div className={job.progress >= 90 ? "text-emerald-400" : "text-zinc-600"}>Knowledge</div>
                            <div className={job.progress >= 95 ? "text-emerald-400" : "text-zinc-600"}>Embeds</div>
                            <div className={job.progress >= 100 ? "text-emerald-400" : "text-zinc-600"}>Ready</div>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                {/* Live Console Terminal Logs */}
                <div className="bg-zinc-900 border border-zinc-850 rounded-2xl p-6 space-y-4">
                  <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <h3 className="text-md font-bold text-white flex items-center gap-2">
                      <Terminal className="w-5 h-5 text-emerald-500" /> Ingestion Terminal Logs
                    </h3>
                    
                    <div className="flex items-center gap-2 text-xs w-full sm:w-auto">
                      <div className="relative flex-1 sm:flex-none">
                        <Search className="w-3.5 h-3.5 text-zinc-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
                        <input
                          type="text"
                          value={terminalSearch}
                          onChange={(e) => setTerminalSearch(e.target.value)}
                          placeholder="Search logs..."
                          className="bg-zinc-950 border border-zinc-800 rounded-lg pl-9.5 pr-3.5 py-1.5 text-xs text-zinc-300 focus:outline-none w-full sm:w-48"
                        />
                      </div>
                      
                      <select
                        value={terminalFilter}
                        onChange={(e) => setTerminalFilter(e.target.value)}
                        className="bg-zinc-950 border border-zinc-800 text-zinc-400 text-xs rounded-lg px-2 py-1.5 focus:outline-none"
                      >
                        <option value="ALL">All</option>
                        <option value="INFO">Info</option>
                        <option value="SUCCESS">Success</option>
                        <option value="WARNING">Warning</option>
                      </select>
                    </div>
                  </div>

                  <div className="bg-zinc-950 p-4.5 rounded-xl border border-zinc-850 h-56 overflow-y-auto font-mono text-[11px] text-zinc-400 space-y-2 scrollbar-thin scrollbar-thumb-zinc-800 select-text">
                    {filteredLogs.map((log, idx) => {
                      let color = "text-zinc-400";
                      if (log.includes("[SUCCESS]")) color = "text-emerald-400";
                      if (log.includes("[WARNING]")) color = "text-amber-400";
                      return (
                        <div key={idx} className={color}>
                          {log}
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>
            )}

            {/* SUB-VIEW 2: Masterpieces Registry */}
            {subTab === "masterpieces" && (
              <div className="space-y-8">
                
                {/* Promote design form */}
                <div className="bg-zinc-900 border border-zinc-850 p-6 rounded-2xl space-y-5">
                  <div>
                    <h3 className="text-md font-bold text-white flex items-center gap-2">
                      <Award className="w-5 h-5 text-amber-400" /> Seed Masterpiece Promotion
                    </h3>
                    <p className="text-xs text-zinc-400 mt-1">
                      Promote outstanding templates to MASTERPIECE status to multiply their RAG search weight.
                    </p>
                  </div>
                  
                  <form onSubmit={promoteToMasterpiece} className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <input
                      type="text"
                      value={newMpName}
                      onChange={(e) => setNewMpName(e.target.value)}
                      placeholder="Masterpiece Name (e.g. NoirFrame)"
                      className="bg-zinc-950 border border-zinc-805 rounded-xl px-4 py-2.5 text-xs text-zinc-300 focus:outline-none focus:border-emerald-500 font-bold"
                    />
                    <input
                      type="text"
                      value={newMpUrl}
                      onChange={(e) => setNewMpUrl(e.target.value)}
                      placeholder="URL (e.g. https://noirframe.com)"
                      className="bg-zinc-950 border border-zinc-805 rounded-xl px-4 py-2.5 text-xs text-zinc-300 focus:outline-none focus:border-emerald-500 font-mono"
                    />
                    <div className="flex gap-2">
                      <select
                        value={newMpCategory}
                        onChange={(e) => setNewMpCategory(e.target.value)}
                        className="bg-zinc-950 border border-zinc-805 text-zinc-400 text-xs rounded-xl px-3 py-2.5 focus:outline-none flex-1"
                      >
                        <option value="luxury">Luxury Design</option>
                        <option value="saas">SaaS UI</option>
                        <option value="threejs">ThreeJS / WebGL</option>
                        <option value="motion">GSAP Motion</option>
                      </select>
                      <button
                        type="submit"
                        className="px-5 py-2.5 rounded-xl bg-emerald-500 text-black hover:bg-emerald-600 font-bold text-xs cursor-pointer flex items-center gap-1.5"
                      >
                        <Plus className="w-4 h-4" /> Promote
                      </button>
                    </div>
                  </form>
                </div>

                {/* Masterpieces Registry Cards Grid */}
                <div className="space-y-4">
                  <h3 className="text-sm font-extrabold uppercase tracking-widest text-zinc-400">
                    Active Masterpiece Reference Sites (Weight = 10)
                  </h3>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                    {masterpieces.map((mp) => (
                      <div key={mp.id} className="bg-zinc-900 border border-zinc-850 p-6 rounded-2xl flex flex-col justify-between h-56 group relative overflow-hidden shadow-sm">
                        <div className="absolute top-0 right-0 w-24 h-24 bg-gradient-to-bl from-amber-500/10 to-transparent rounded-bl-full pointer-events-none group-hover:from-amber-500/15 transition-all" />
                        
                        <div className="space-y-3">
                          <div className="flex justify-between items-start">
                            <div>
                              <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/10 border border-amber-500/20 text-amber-400 uppercase tracking-widest inline-flex items-center gap-1">
                                <Award className="w-3 h-3" /> Masterpiece
                              </span>
                              <h4 className="text-base font-bold text-white mt-2 font-display italic tracking-wide group-hover:text-emerald-400 transition-colors">
                                {mp.name}
                              </h4>
                            </div>
                            
                            <div className="text-right">
                              <span className="text-2xl font-extrabold text-amber-400 block font-display">
                                {mp.score}
                              </span>
                              <span className="text-[9px] text-zinc-550 font-bold uppercase tracking-wider block mt-0.5">Rating Score</span>
                            </div>
                          </div>

                          <div className="flex flex-wrap gap-1.5">
                            {mp.category.map((cat: string) => (
                              <span key={cat} className="text-[9px] font-mono font-bold tracking-wider px-2 py-0.5 rounded bg-zinc-950 border border-zinc-800 text-zinc-450 uppercase">
                                {cat}
                              </span>
                            ))}
                          </div>

                          <p className="text-[10px] text-zinc-500 font-mono truncate pt-1">{mp.url}</p>
                        </div>

                        <div className="flex justify-between items-center border-t border-zinc-800/40 pt-4.5">
                          <a
                            href={mp.url}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-[10px] font-bold text-zinc-400 hover:text-white flex items-center gap-1 group/link"
                          >
                            Visit Reference <ArrowUpRight className="w-3 h-3 group-hover/link:translate-x-0.5 group-hover/link:-translate-y-0.5 transition-transform" />
                          </a>
                          
                          <button
                            onClick={() => demoteMasterpiece(mp.url)}
                            className="text-[10px] font-bold text-red-400 hover:text-red-300 flex items-center gap-1 cursor-pointer bg-transparent border-none"
                          >
                            <Trash2 className="w-3.5 h-3.5" /> Demote URL
                          </button>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>
            )}

            {/* SUB-VIEW 3: Library Explorer Tree */}
            {subTab === "explorer" && (
              <div className="space-y-6">
                <div className="flex justify-between items-center">
                  <div>
                    <h3 className="text-md font-bold text-white flex items-center gap-2">
                      <FolderDot className="w-5 h-5 text-emerald-500" /> Ingested Library Explorer
                    </h3>
                    <p className="text-xs text-zinc-400 mt-1">
                      Browse layout components, styles, gradients, and prompt configurations synced in the databases.
                    </p>
                  </div>
                  <button
                    onClick={fetchFiles}
                    className="px-3.5 py-1.5 rounded-lg bg-zinc-900 border border-zinc-800 text-zinc-400 hover:text-white hover:border-zinc-700 transition-all cursor-pointer flex items-center gap-2 text-xs font-bold"
                  >
                    <RefreshCw className={`w-3.5 h-3.5 ${loadingFiles ? "animate-spin" : ""}`} /> Refresh Library
                  </button>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {Object.entries(groupedFiles).map(([category, files]) => (
                    <div key={category} className="bg-zinc-900 border border-zinc-800/80 rounded-2xl p-5 flex flex-col justify-between h-72">
                      <div>
                        <div className="flex justify-between items-center mb-4 border-b border-zinc-850 pb-3">
                          <div className="flex items-center gap-2">
                            {getFolderIcon(category)}
                            <span className="text-xs font-extrabold capitalize text-white tracking-wide">
                              {category.replace("_", " ")}
                            </span>
                          </div>
                          <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-zinc-950 text-zinc-400 border border-zinc-850">
                            {files.length}
                          </span>
                        </div>

                        <div className="overflow-y-auto max-h-40 space-y-2 pr-1.5 scrollbar-thin scrollbar-thumb-zinc-800">
                          {files.length === 0 ? (
                            <span className="text-[10px] text-zinc-600 block text-center mt-10 italic font-medium">
                              No items compiled yet
                            </span>
                          ) : (
                            (files as MonitoredFile[]).map((file: MonitoredFile, idx: number) => (
                              <div key={idx} className="flex justify-between items-center p-2 rounded-lg bg-zinc-950 border border-zinc-850 hover:border-zinc-800 transition-colors">
                                <span className="text-[11px] truncate font-mono text-zinc-300 font-semibold max-w-[120px]" title={file.name}>
                                  {file.name}
                                </span>
                                <span className="text-[9px] font-mono text-zinc-550">
                                  {formatSize(file.size)}
                                </span>
                              </div>
                            ))
                          )}
                        </div>
                      </div>
                      
                      <div className="border-t border-zinc-850 pt-3 text-[9px] font-mono text-zinc-550 uppercase flex justify-between tracking-wider">
                        <span>REPOSITORY TARGET</span>
                        <span>/knowledge_input/{category}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* SUB-VIEW 4: Growth & Ingestion Analytics */}
            {subTab === "analytics" && (
              <div className="space-y-8">
                
                {/* Visual Area Chart for growth trend */}
                <div className="bg-zinc-900 border border-zinc-850 p-6 rounded-2xl space-y-4">
                  <h3 className="text-md font-bold text-white flex items-center gap-2">
                    <Activity className="w-5 h-5 text-emerald-500" /> Weekly Knowledge Growth Trend
                  </h3>
                  
                  <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                      <AreaChart data={analyticsData} margin={{ top: 10, right: 10, left: -25, bottom: 0 }}>
                        <defs>
                          <linearGradient id="colorImports" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                            <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                          </linearGradient>
                          <linearGradient id="colorComponents" x1="0" y1="0" x2="0" y2="1">
                            <stop offset="5%" stopColor="#38bdf8" stopOpacity={0.2} />
                            <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
                          </linearGradient>
                        </defs>
                        <CartesianGrid strokeDasharray="3 3" stroke="#27272a" vertical={false} />
                        <XAxis dataKey="name" stroke="#52525b" fontSize={10} tickLine={false} />
                        <YAxis stroke="#52525b" fontSize={10} tickLine={false} />
                        <ChartTooltip
                          contentStyle={{ backgroundColor: "#09090b", borderColor: "#27272a", borderRadius: "8px", fontSize: "11px" }}
                        />
                        <Area type="monotone" dataKey="imports" name="Websites Crawled" stroke="#10b981" fillOpacity={1} fill="url(#colorImports)" strokeWidth={2} />
                        <Area type="monotone" dataKey="components" name="Synthesized Components" stroke="#38bdf8" fillOpacity={1} fill="url(#colorComponents)" strokeWidth={2} />
                      </AreaChart>
                    </ResponsiveContainer>
                  </div>
                </div>

                {/* Pie Chart and list data grid */}
                <div className="grid grid-cols-1 md:grid-cols-12 gap-8">
                  {/* Pie chart */}
                  <div className="md:col-span-5 bg-zinc-900 border border-zinc-850 p-6 rounded-2xl flex flex-col items-center justify-center">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500 mb-4 w-full text-left">
                      Category Distribution
                    </h3>
                    <div className="h-48 w-full flex items-center justify-center">
                      <ResponsiveContainer width="100%" height="100%">
                        <PieChart>
                          <Pie
                            data={categoriesPieData}
                            cx="50%"
                            cy="50%"
                            innerRadius={60}
                            outerRadius={80}
                            paddingAngle={5}
                            dataKey="value"
                          >
                            {categoriesPieData.map((entry, index) => (
                              <Cell key={`cell-${index}`} fill={entry.color} />
                            ))}
                          </Pie>
                        </PieChart>
                      </ResponsiveContainer>
                    </div>
                  </div>

                  {/* List legends */}
                  <div className="md:col-span-7 bg-zinc-900 border border-zinc-850 p-6 rounded-2xl flex flex-col justify-center space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-zinc-500">
                      Distribution Details
                    </h3>
                    <div className="space-y-3">
                      {categoriesPieData.map((item, idx) => (
                        <div key={idx} className="flex justify-between items-center text-xs font-semibold">
                          <div className="flex items-center gap-3">
                            <span className="w-3 h-3 rounded-full" style={{ backgroundColor: item.color }} />
                            <span className="text-zinc-350">{item.name}</span>
                          </div>
                          <span className="text-white font-mono">{item.value} items</span>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* SUB-VIEW 5: Crawlers Configuration Settings */}
            {subTab === "settings" && (
              <div className="bg-zinc-900 border border-zinc-850 p-6 rounded-2xl space-y-6">
                <div>
                  <h3 className="text-md font-bold text-white flex items-center gap-2">
                    <Sliders className="w-5 h-5 text-emerald-500" /> Crawler Engine Settings
                  </h3>
                  <p className="text-xs text-zinc-400 mt-1">
                    Fine-tune crawling timing, whitelist regexes, default AI plan generators models, and priority RAG weight configurations.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 border-t border-zinc-850 pt-6">
                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 block">Watchdog Scan Interval (seconds)</label>
                    <input
                      type="number"
                      value={settings.scanInterval}
                      onChange={(e) => setSettings({ ...settings, scanInterval: parseInt(e.target.value) || 2 })}
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-2 text-xs text-zinc-300 focus:outline-none"
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 block">OpenAI / Gemini Model Target</label>
                    <select
                      value={settings.aiModel}
                      onChange={(e) => setSettings({ ...settings, aiModel: e.target.value })}
                      className="w-full bg-zinc-950 border border-zinc-800 text-zinc-400 text-xs rounded-xl px-3 py-2.5 focus:outline-none"
                    >
                      <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
                      <option value="gpt-4o-mini">GPT-4o Mini</option>
                      <option value="claude-3-5-sonnet">Claude 3.5 Sonnet</option>
                    </select>
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 block">Priority Masterpieces Weight Weight</label>
                    <input
                      type="number"
                      value={settings.priorityWeight}
                      onChange={(e) => setSettings({ ...settings, priorityWeight: parseInt(e.target.value) || 10 })}
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-2 text-xs text-zinc-300 focus:outline-none"
                    />
                  </div>

                  <div className="space-y-2">
                    <label className="text-xs font-bold text-zinc-400 block">Domains Whitelist (comma-separated)</label>
                    <input
                      type="text"
                      value={settings.domainWhitelist}
                      onChange={(e) => setSettings({ ...settings, domainWhitelist: e.target.value })}
                      className="w-full bg-zinc-950 border border-zinc-800 rounded-xl px-4 py-2 text-xs text-zinc-300 focus:outline-none font-mono"
                    />
                  </div>
                </div>

                <div className="border-t border-zinc-850 pt-5 flex justify-end">
                  <button
                    onClick={() => addLog("[SYSTEM] Settings updated successfully.")}
                    className="px-6 py-2.5 rounded-xl bg-emerald-500 text-black hover:bg-emerald-600 font-bold text-xs cursor-pointer shadow-md shadow-emerald-500/10"
                  >
                    Save Configuration
                  </button>
                </div>
              </div>
            )}
          </motion.div>
        </AnimatePresence>
      </div>
    </div>
  );
}
