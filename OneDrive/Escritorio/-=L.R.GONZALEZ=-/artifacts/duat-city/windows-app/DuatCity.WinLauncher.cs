using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Net;
using System.Net.Sockets;
using System.Security.Cryptography;
using System.Text;
using System.Threading;

namespace DuatCityWinApp
{
    internal static class Program
    {
        private const string Fingerprint = "DUAT-v1.4-WINAPP-CONVERSION";

        public static int Main(string[] args)
        {
            try
            {
                Options options = Options.Parse(args);
                string exeDir = AppDomain.CurrentDomain.BaseDirectory;
                string appDir = Path.GetFullPath(options.AppDir ?? Path.Combine(exeDir, "app"));
                string edgePath = FindEdge();

                if (!Directory.Exists(appDir) || !File.Exists(Path.Combine(appDir, "index.html")))
                {
                    Console.Error.WriteLine("DUAT_WINAPP_ERROR app directory missing index.html: " + appDir);
                    return 2;
                }

                if (options.Smoke)
                {
                    Console.WriteLine(RenderSmokeJson(appDir, edgePath));
                    return 0;
                }

                int port = options.Port > 0 ? options.Port : FindFreePort();
                StaticFileServer server = new StaticFileServer(appDir, port);
                server.Start();
                string url = "http://127.0.0.1:" + port + "/duat-city/?nativeWin=1";
                Console.WriteLine("DUAT_WINAPP_URL=" + url);
                Console.Out.Flush();

                if (!options.ServeOnly)
                {
                    Process edge = LaunchEdge(edgePath, url);
                    Console.WriteLine("DUAT_WINAPP_EDGE_PID=" + edge.Id);
                    while (!edge.HasExited)
                    {
                        Thread.Sleep(500);
                    }
                    server.Stop();
                    return 0;
                }

                if (options.DurationMs > 0)
                {
                    Thread.Sleep(options.DurationMs);
                    server.Stop();
                    Environment.Exit(0);
                }

                Console.WriteLine("DUAT_WINAPP_SERVE_ONLY=1");
                Console.Out.Flush();
                while (true)
                {
                    Thread.Sleep(1000);
                }
            }
            catch (Exception ex)
            {
                Console.Error.WriteLine("DUAT_WINAPP_ERROR " + ex.GetType().Name + ": " + ex.Message);
                return 1;
            }
        }

        private static Process LaunchEdge(string edgePath, string url)
        {
            ProcessStartInfo info = new ProcessStartInfo();
            info.FileName = edgePath;
            info.Arguments = "--app=\"" + url + "\" --no-first-run --no-default-browser-check --disable-sync --autoplay-policy=user-gesture-required";
            info.UseShellExecute = false;
            return Process.Start(info);
        }

        private static string FindEdge()
        {
            string[] candidates = new string[]
            {
                @"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
                @"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
            };
            foreach (string candidate in candidates)
            {
                if (File.Exists(candidate))
                {
                    return candidate;
                }
            }
            throw new FileNotFoundException("Microsoft Edge executable not found.");
        }

        private static int FindFreePort()
        {
            TcpListener listener = new TcpListener(IPAddress.Loopback, 0);
            listener.Start();
            int port = ((IPEndPoint)listener.LocalEndpoint).Port;
            listener.Stop();
            return port;
        }

        private static string RenderSmokeJson(string appDir, string edgePath)
        {
            int fileCount = Directory.GetFiles(appDir, "*", SearchOption.AllDirectories).Length;
            return "{"
                + "\"schema\":\"duat/windows-app-smoke/v1.4\","
                + "\"fingerprint\":\"" + Fingerprint + "\","
                + "\"status\":\"OK\","
                + "\"app_dir\":\"" + JsonEscape(appDir) + "\","
                + "\"edge_path\":\"" + JsonEscape(edgePath) + "\","
                + "\"file_count\":" + fileCount + ","
                + "\"publication_allowed\":false,"
                + "\"cloud_used\":false,"
                + "\"wabi_execution_allowed\":false"
                + "}";
        }

        private static string JsonEscape(string value)
        {
            return value.Replace("\\", "\\\\").Replace("\"", "\\\"");
        }
    }

    internal sealed class Options
    {
        public bool Smoke;
        public bool ServeOnly;
        public int Port;
        public int DurationMs;
        public string AppDir;

        public static Options Parse(string[] args)
        {
            Options options = new Options();
            for (int i = 0; i < args.Length; i++)
            {
                string arg = args[i];
                if (arg == "--smoke") options.Smoke = true;
                else if (arg == "--serve-only") options.ServeOnly = true;
                else if (arg == "--port" && i + 1 < args.Length) options.Port = ParseInt(args[++i]);
                else if (arg == "--duration-ms" && i + 1 < args.Length) options.DurationMs = ParseInt(args[++i]);
                else if (arg == "--app-dir" && i + 1 < args.Length) options.AppDir = args[++i];
            }
            return options;
        }

        private static int ParseInt(string value)
        {
            int parsed;
            return int.TryParse(value, out parsed) ? parsed : 0;
        }
    }

    internal sealed class StaticFileServer
    {
        private readonly string root;
        private readonly int port;
        private TcpListener listener;
        private bool running;

        public StaticFileServer(string root, int port)
        {
            this.root = Path.GetFullPath(root);
            this.port = port;
        }

        public void Start()
        {
            listener = new TcpListener(IPAddress.Loopback, port);
            listener.Start();
            running = true;
            Thread thread = new Thread(AcceptLoop);
            thread.IsBackground = true;
            thread.Start();
        }

        public void Stop()
        {
            running = false;
            try { listener.Stop(); } catch { }
        }

        private void AcceptLoop()
        {
            while (running)
            {
                try
                {
                    TcpClient client = listener.AcceptTcpClient();
                    ThreadPool.QueueUserWorkItem(HandleClient, client);
                }
                catch
                {
                    if (running) Thread.Sleep(50);
                }
            }
        }

        private void HandleClient(object state)
        {
            TcpClient client = (TcpClient)state;
            using (client)
            {
                NetworkStream stream = client.GetStream();
                string request = ReadRequest(stream);
                string path = ParsePath(request);
                string filePath = ResolvePath(path);
                if (filePath == null)
                {
                    WriteResponse(stream, 404, "text/plain; charset=utf-8", Encoding.UTF8.GetBytes("not found"));
                    return;
                }
                byte[] body = File.ReadAllBytes(filePath);
                WriteResponse(stream, 200, ContentType(filePath), body);
            }
        }

        private string ReadRequest(NetworkStream stream)
        {
            byte[] buffer = new byte[8192];
            int read = stream.Read(buffer, 0, buffer.Length);
            if (read <= 0) return "";
            return Encoding.ASCII.GetString(buffer, 0, read);
        }

        private string ParsePath(string request)
        {
            string[] lines = request.Split(new string[] { "\r\n" }, StringSplitOptions.None);
            if (lines.Length == 0) return "/";
            string[] parts = lines[0].Split(' ');
            if (parts.Length < 2) return "/";
            string path = parts[1];
            int query = path.IndexOf('?');
            if (query >= 0) path = path.Substring(0, query);
            return Uri.UnescapeDataString(path);
        }

        private string ResolvePath(string requestPath)
        {
            string path = requestPath;
            if (path == "/duat-city") path = "/";
            if (path.StartsWith("/duat-city/", StringComparison.OrdinalIgnoreCase))
            {
                path = path.Substring("/duat-city".Length);
            }
            if (path == "/") path = "/index.html";

            string candidate = Path.GetFullPath(Path.Combine(root, path.TrimStart('/').Replace('/', Path.DirectorySeparatorChar)));
            if (!candidate.StartsWith(root, StringComparison.OrdinalIgnoreCase))
            {
                return null;
            }
            if (File.Exists(candidate))
            {
                return candidate;
            }
            if (String.IsNullOrEmpty(Path.GetExtension(candidate)))
            {
                string index = Path.Combine(root, "index.html");
                if (File.Exists(index)) return index;
            }
            return null;
        }

        private void WriteResponse(NetworkStream stream, int status, string contentType, byte[] body)
        {
            string statusText = status == 200 ? "OK" : "Not Found";
            string header = "HTTP/1.1 " + status + " " + statusText + "\r\n"
                + "Content-Type: " + contentType + "\r\n"
                + "Content-Length: " + body.Length + "\r\n"
                + "Cache-Control: no-store\r\n"
                + "Connection: close\r\n\r\n";
            byte[] headerBytes = Encoding.ASCII.GetBytes(header);
            stream.Write(headerBytes, 0, headerBytes.Length);
            stream.Write(body, 0, body.Length);
        }

        private string ContentType(string path)
        {
            string ext = Path.GetExtension(path).ToLowerInvariant();
            if (ext == ".html") return "text/html; charset=utf-8";
            if (ext == ".js") return "text/javascript; charset=utf-8";
            if (ext == ".css") return "text/css; charset=utf-8";
            if (ext == ".json") return "application/json; charset=utf-8";
            if (ext == ".svg") return "image/svg+xml";
            if (ext == ".png") return "image/png";
            if (ext == ".jpg" || ext == ".jpeg") return "image/jpeg";
            if (ext == ".webp") return "image/webp";
            if (ext == ".ico") return "image/x-icon";
            if (ext == ".txt") return "text/plain; charset=utf-8";
            return "application/octet-stream";
        }
    }
}
