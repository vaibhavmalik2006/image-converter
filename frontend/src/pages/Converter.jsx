import { useState } from 'react'
import { Link } from 'react-router-dom'
import { changeDpi, compressImage, convertImage, downloadFile, resizeImage, uploadImage } from '../services/api'

function Converter() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [fileId, setFileId] = useState('')
  const [outputFormat, setOutputFormat] = useState('PNG')
  const [width, setWidth] = useState('')
  const [height, setHeight] = useState('')
  const [keepAspectRatio, setKeepAspectRatio] = useState(true)
  const [dpi, setDpi] = useState('300')
  const [quality, setQuality] = useState(90)
  const [targetSize, setTargetSize] = useState('')
  const [loading, setLoading] = useState(false)
  const [status, setStatus] = useState('')
  const [error, setError] = useState('')

  const handleFileChange = async (selectedFile) => {
    setFile(selectedFile)
    setPreviewUrl(URL.createObjectURL(selectedFile))
    setLoading(true)
    setError('')
    try {
      const response = await uploadImage(selectedFile)
      setFileId(response.data.id)
      setStatus('Image uploaded successfully')
    } catch (err) {
      setError('Upload failed. Please try another image.')
    } finally {
      setLoading(false)
    }
  }

  const handleConvert = async () => {
    if (!fileId) {
      setError('Upload an image first.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const params = {
        file_id: fileId,
        output_format: outputFormat,
        width: width ? Number(width) : null,
        height: height ? Number(height) : null,
        keep_aspect_ratio: keepAspectRatio,
        dpi: Number(dpi),
        quality,
        target_size_kb: targetSize ? Number(targetSize) : null,
      }
      const response = await convertImage(params)
      const blob = new Blob([response.data], { type: response.headers['content-type'] || 'application/octet-stream' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const extension = outputFormat.toLowerCase() === 'jpg' ? 'jpg' : outputFormat.toLowerCase()
      link.download = `converted.${extension}`
      link.click()
      URL.revokeObjectURL(url)
      setStatus('Image converted and downloaded')
    } catch (err) {
      setError('Conversion failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleResize = async () => {
    if (!fileId) {
      setError('Upload an image first.')
      return
    }
    setLoading(true)
    try {
      const response = await resizeImage({ file_id: fileId, width: Number(width || 0), height: Number(height || 0), keep_aspect_ratio: keepAspectRatio, output_format: outputFormat, dpi: Number(dpi) })
      const blob = new Blob([response.data], { type: response.headers['content-type'] || 'application/octet-stream' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const resizedExtension = outputFormat.toLowerCase() === 'jpg' ? 'jpg' : outputFormat.toLowerCase()
      link.download = `resized.${resizedExtension}`
      link.click()
      URL.revokeObjectURL(url)
      setStatus('Resize applied')
    } catch (err) {
      setError('Resize failed')
    } finally {
      setLoading(false)
    }
  }

  const handleCompress = async () => {
    if (!fileId) {
      setError('Upload an image first.')
      return
    }
    setLoading(true)
    try {
      const response = await compressImage({ file_id: fileId, quality, target_size_kb: targetSize ? Number(targetSize) : null, output_format: outputFormat, dpi: Number(dpi) })
      const blob = new Blob([response.data], { type: response.headers['content-type'] || 'application/octet-stream' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const compressedExtension = outputFormat.toLowerCase() === 'jpg' ? 'jpg' : outputFormat.toLowerCase()
      link.download = `compressed.${compressedExtension}`
      link.click()
      URL.revokeObjectURL(url)
      setStatus('Compression applied')
    } catch (err) {
      setError('Compression failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDpi = async () => {
    if (!fileId) {
      setError('Upload an image first.')
      return
    }
    setLoading(true)
    try {
      const response = await changeDpi({ file_id: fileId, dpi: Number(dpi), output_format: outputFormat, quality })
      const blob = new Blob([response.data], { type: response.headers['content-type'] || 'application/octet-stream' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const dpiExtension = outputFormat.toLowerCase() === 'jpg' ? 'jpg' : outputFormat.toLowerCase()
      link.download = `dpi.${dpiExtension}`
      link.click()
      URL.revokeObjectURL(url)
      setStatus('DPI updated')
    } catch (err) {
      setError('DPI update failed')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = async () => {
    if (!fileId) {
      setError('Upload an image first.')
      return
    }
    setLoading(true)
    setError('')
    try {
      const params = {
        file_id: fileId,
        output_format: outputFormat,
        width: width ? Number(width) : null,
        height: height ? Number(height) : null,
        keep_aspect_ratio: keepAspectRatio,
        dpi: Number(dpi),
        quality,
        target_size_kb: targetSize ? Number(targetSize) : null,
      }
      const response = await downloadFile(fileId, params)
      const blob = new Blob([response.data], { type: response.headers['content-type'] || 'application/octet-stream' })
      const url = URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const extension = outputFormat.toLowerCase() === 'jpg' ? 'jpg' : outputFormat.toLowerCase()
      link.download = `processed.${extension}`
      link.click()
      URL.revokeObjectURL(url)
      setStatus('Processed image downloaded successfully')
    } catch (err) {
      setError('Download failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="mx-auto flex max-w-7xl items-center justify-between px-6 py-6 lg:px-8">
        <Link to="/" className="text-xl font-semibold">AI Image Converter</Link>
      </header>

      <main className="mx-auto grid max-w-7xl gap-8 px-6 pb-12 lg:grid-cols-[0.95fr_1.05fr] lg:px-8">
        <section className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-cyan-950/20">
          <h2 className="text-2xl font-semibold">Upload & Preview</h2>
          <label className="mt-6 flex cursor-pointer flex-col items-center justify-center rounded-2xl border border-dashed border-cyan-500/40 bg-slate-900/70 p-10 text-center transition hover:border-cyan-400">
            <input type="file" accept="image/*" className="hidden" onChange={(e) => handleFileChange(e.target.files[0])} />
            <p className="text-lg font-medium text-cyan-300">Drop your image here</p>
            <p className="mt-2 text-sm text-slate-400">PNG, JPG, BMP, WEBP, GIF, TIFF, ICO</p>
          </label>
          {previewUrl ? (
            <div className="mt-6 overflow-hidden rounded-2xl border border-white/10 bg-slate-900/80 p-4">
              <img src={previewUrl} alt="Preview" className="mx-auto max-h-80 object-contain" />
            </div>
          ) : null}
        </section>

        <section className="rounded-3xl border border-white/10 bg-white/5 p-6 shadow-2xl shadow-cyan-950/20">
          <h2 className="text-2xl font-semibold">Settings</h2>
          <div className="mt-6 grid gap-4 md:grid-cols-2">
            <label className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <span className="mb-2 block text-sm text-slate-400">Output Format</span>
              <select value={outputFormat} onChange={(e) => setOutputFormat(e.target.value)} className="w-full rounded-lg bg-slate-800 px-3 py-2 text-slate-100">
                <option value="PNG">PNG</option>
                <option value="JPG">JPG</option>
                <option value="WEBP">WEBP</option>
                <option value="BMP">BMP</option>
              </select>
            </label>

            <label className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <span className="mb-2 block text-sm text-slate-400">Width (px)</span>
              <input type="number" value={width} onChange={(e) => setWidth(e.target.value)} className="w-full rounded-lg bg-slate-800 px-3 py-2 text-slate-100" />
            </label>

            <label className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <span className="mb-2 block text-sm text-slate-400">Height (px)</span>
              <input type="number" value={height} onChange={(e) => setHeight(e.target.value)} className="w-full rounded-lg bg-slate-800 px-3 py-2 text-slate-100" />
            </label>

            <label className="flex items-center justify-between rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <span className="text-sm text-slate-400">Keep Aspect Ratio</span>
              <input type="checkbox" checked={keepAspectRatio} onChange={() => setKeepAspectRatio(!keepAspectRatio)} className="h-4 w-4" />
            </label>

            <label className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <span className="mb-2 block text-sm text-slate-400">DPI</span>
              <select value={dpi} onChange={(e) => setDpi(e.target.value)} className="w-full rounded-lg bg-slate-800 px-3 py-2 text-slate-100">
                <option value="72">72</option>
                <option value="96">96</option>
                <option value="150">150</option>
                <option value="300">300</option>
                <option value="600">600</option>
              </select>
            </label>

            <label className="rounded-2xl border border-white/10 bg-slate-900/70 p-4">
              <span className="mb-2 block text-sm text-slate-400">Target File Size (KB)</span>
              <input type="number" value={targetSize} onChange={(e) => setTargetSize(e.target.value)} className="w-full rounded-lg bg-slate-800 px-3 py-2 text-slate-100" placeholder="100" />
            </label>
          </div>

          <label className="mt-4 block rounded-2xl border border-white/10 bg-slate-900/70 p-4">
            <div className="mb-2 flex items-center justify-between text-sm text-slate-400">
              <span>Quality</span>
              <span>{quality}%</span>
            </div>
            <input type="range" min="0" max="100" value={quality} onChange={(e) => setQuality(Number(e.target.value))} className="w-full" />
          </label>

          <div className="mt-6 flex flex-wrap gap-3">
            <button onClick={handleConvert} className="rounded-full bg-cyan-500 px-5 py-2 font-semibold text-slate-950 transition hover:bg-cyan-400">Convert</button>
            <button onClick={handleResize} className="rounded-full border border-white/15 px-5 py-2 font-semibold text-slate-200 transition hover:border-cyan-400">Resize</button>
            <button onClick={handleCompress} className="rounded-full border border-white/15 px-5 py-2 font-semibold text-slate-200 transition hover:border-cyan-400">Compress</button>
            <button onClick={handleDpi} className="rounded-full border border-white/15 px-5 py-2 font-semibold text-slate-200 transition hover:border-cyan-400">Set DPI</button>
            <button onClick={handleDownload} className="rounded-full border border-cyan-500/30 px-5 py-2 font-semibold text-cyan-300 transition hover:border-cyan-400">Download</button>
          </div>

          {loading ? <p className="mt-4 text-sm text-cyan-300">Processing image...</p> : null}
          {status ? <p className="mt-4 text-sm text-emerald-400">{status}</p> : null}
          {error ? <p className="mt-4 text-sm text-rose-400">{error}</p> : null}
        </section>
      </main>
    </div>
  )
}

export default Converter
