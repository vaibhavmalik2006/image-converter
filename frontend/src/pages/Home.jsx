import { Link } from 'react-router-dom'

const features = [
  'Upload JPG, PNG, BMP, GIF, WEBP, TIFF, and ICO files',
  'Convert formats and resize while keeping aspect ratio',
  'Set DPI, quality, and compress to a target file size',
  'Download instantly without storing images permanently',
]

function Home() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <div className="text-xl font-semibold">AI Image Converter</div>
        <Link to="/converter" className="rounded-full bg-cyan-500 px-4 py-2 font-medium text-slate-950 transition hover:bg-cyan-400">Open Converter</Link>
      </header>

      <main className="mx-auto max-w-7xl px-6 pb-20 lg:px-8">
        <section className="grid items-center gap-10 rounded-3xl border border-white/10 bg-white/5 p-8 shadow-2xl shadow-cyan-950/20 lg:grid-cols-[1.1fr_0.9fr] lg:p-16">
          <div>
            <p className="mb-4 inline-flex rounded-full border border-cyan-500/30 bg-cyan-500/10 px-3 py-1 text-sm text-cyan-300">Fast • Secure • Modern</p>
            <h1 className="text-4xl font-semibold leading-tight sm:text-5xl">Convert, resize, and compress images in one elegant workflow.</h1>
            <p className="mt-6 max-w-2xl text-lg text-slate-300">Upload an image, adjust output settings, and download a polished version instantly. All processing is temporary and never stored permanently.</p>
            <div className="mt-8 flex flex-wrap gap-4">
              <Link to="/converter" className="rounded-full bg-cyan-500 px-6 py-3 font-semibold text-slate-950 transition hover:bg-cyan-400">Start Converting</Link>
              <a href="#features" className="rounded-full border border-white/15 px-6 py-3 font-semibold text-slate-200 transition hover:border-cyan-400">Explore Features</a>
            </div>
          </div>
          <div className="rounded-2xl border border-cyan-500/20 bg-slate-900/80 p-6 shadow-lg">
            <div className="rounded-xl border border-dashed border-cyan-500/40 p-8 text-center">
              <p className="text-lg font-medium text-cyan-300">Drag & Drop Upload</p>
              <p className="mt-3 text-sm text-slate-400">JPG, PNG, GIF, WEBP, BMP, TIFF, and ICO support</p>
            </div>
          </div>
        </section>

        <section id="features" className="mt-16 grid gap-6 md:grid-cols-2 xl:grid-cols-4">
          {features.map((feature) => (
            <div key={feature} className="rounded-2xl border border-white/10 bg-white/5 p-6">
              <div className="mb-4 h-10 w-10 rounded-full bg-cyan-500/15" />
              <p className="text-slate-200">{feature}</p>
            </div>
          ))}
        </section>
      </main>

      <footer className="border-t border-white/10 py-6 text-center text-sm text-slate-400">Built with React, Vite, Tailwind, FastAPI, Pillow, and PostgreSQL.</footer>
    </div>
  )
}

export default Home
