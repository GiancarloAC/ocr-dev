import { useState, useEffect } from 'react'
import './index.css'

function App() {
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    if (darkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [darkMode]);

  return (
    <div className="bg-background text-on-background font-body-md text-body-md antialiased min-h-screen flex flex-col transition-colors duration-200">
      <nav className="bg-background/80 backdrop-blur-md border-b border-outline-variant w-full top-0 sticky z-50">
        <div className="flex justify-between items-center w-full px-gutter max-w-container-max mx-auto h-16">
          <div className="flex items-center gap-2">
            <span className="font-headline-lg text-headline-lg font-bold text-on-background tracking-tighter hidden sm:block">OCR.dev</span>
          </div>
          <div className="hidden md:flex gap-8">
            <a className="text-on-surface-variant hover:text-primary transition-colors duration-200 active:scale-95 duration-150 font-label-caps text-label-caps" href="#">Features</a>
            <a className="text-on-surface-variant hover:text-primary transition-colors duration-200 active:scale-95 duration-150 font-label-caps text-label-caps" href="#">API Docs</a>
          </div>
          <div className="flex items-center gap-4">
            <button className="font-label-caps text-label-caps text-on-surface-variant hover:text-primary transition-colors duration-200 active:scale-95 duration-150 hidden sm:block">GitHub</button>
            <div className="flex items-center gap-2 border-l border-outline-variant pl-4">
              <button aria-label="GitHub" className="text-on-surface-variant hover:text-primary transition-colors duration-200 active:scale-95 duration-150 flex items-center justify-center h-8 w-8 rounded-full">
                <span className="material-symbols-outlined" data-icon="github">code</span>
              </button>
              <button aria-label="Toggle Dark Mode" onClick={() => setDarkMode(!darkMode)} className="text-on-surface-variant hover:text-primary transition-colors duration-200 active:scale-95 duration-150 flex items-center justify-center h-8 w-8 rounded-full">
                <span className="material-symbols-outlined" data-icon="dark_mode">{darkMode ? 'light_mode' : 'dark_mode'}</span>
              </button>
            </div>
          </div>
        </div>
      </nav>
      
      <main className="flex-grow flex flex-col gap-16 py-12 w-full px-gutter max-w-container-max mx-auto">
        <section className="max-w-3xl mx-auto w-full text-center flex flex-col gap-8">
          <div>
            <h1 className="font-display text-display text-on-surface mb-2">Visual Intelligence</h1>
            <p className="font-body-md text-body-md text-on-surface-variant">Extract structured data from raw documents instantly.</p>
          </div>
          <div className="relative border-2 border-dashed border-outline-variant rounded-xl bg-surface-container-low hover:bg-surface-container transition-colors duration-200 p-12 flex flex-col items-center justify-center gap-4 cursor-pointer overflow-hidden group">
            <div className="absolute inset-0 bg-inverse-primary/0 group-hover:bg-inverse-primary/5 transition-colors duration-300"></div>
            <div className="h-16 w-16 rounded-full bg-surface-variant flex items-center justify-center text-outline group-hover:text-inverse-primary group-hover:scale-110 transition-all duration-300">
              <span className="material-symbols-outlined text-3xl" data-icon="upload_file">upload_file</span>
            </div>
            <div className="flex flex-col gap-1 z-10">
              <p className="font-body-md text-body-md text-on-surface font-semibold">Drag and drop document, or click to browse</p>
              <p className="font-label-caps text-label-caps text-outline">Supported: PDF, PNG, JPG (Max 10MB)</p>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 lg:grid-cols-12 gap-gutter">
          <div className="lg:col-span-5 flex flex-col gap-4">
            <div className="flex items-center justify-between">
              <h2 className="font-body-md text-body-md font-semibold text-on-surface">Source Document</h2>
              <span className="font-label-caps text-label-caps text-primary bg-primary/10 px-2 py-1 rounded-full">Processing Complete</span>
            </div>
            <div className="bg-surface-container-low border border-outline-variant rounded-xl p-4 aspect-[3/4] flex items-center justify-center relative overflow-hidden group">
              <div className="absolute inset-0 bg-surface-container/50 backdrop-blur-sm opacity-0 group-hover:opacity-100 transition-opacity duration-300 flex items-center justify-center z-10">
                <button className="bg-inverse-primary text-white font-label-caps text-label-caps px-4 py-2 rounded-lg hover:opacity-90 transition-opacity flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm" data-icon="zoom_in">zoom_in</span> View Full Size
                </button>
              </div>
              <div className="w-full h-full bg-[radial-gradient(ellipse_at_center,_var(--tw-gradient-stops))] from-surface-variant to-background opacity-20 border border-outline-variant/30 relative">
                <div className="absolute top-4 left-4 right-4 h-8 bg-surface-variant/40 rounded"></div>
                <div className="absolute top-16 left-4 w-1/2 h-4 bg-surface-variant/40 rounded"></div>
                <div className="absolute top-24 left-4 right-4 h-32 bg-surface-variant/30 border border-surface-variant/50"></div>
                <div className="absolute bottom-4 right-4 w-1/3 h-6 bg-surface-variant/40 rounded"></div>
              </div>
            </div>
          </div>
          
          <div className="lg:col-span-7 flex flex-col gap-4">
            <div className="flex items-center justify-between border-b border-outline-variant pb-2">
              <div className="flex gap-6">
                <button className="font-label-caps text-label-caps text-on-surface-variant pb-2 border-b-2 border-transparent hover:text-on-surface transition-colors">Text</button>
                <button className="font-label-caps text-label-caps text-inverse-primary pb-2 border-b-2 border-inverse-primary">JSON</button>
                <button className="font-label-caps text-label-caps text-on-surface-variant pb-2 border-b-2 border-transparent hover:text-on-surface transition-colors">Table</button>
              </div>
              <div className="flex gap-2">
                <button className="text-on-surface-variant hover:text-on-surface p-1 rounded hover:bg-surface-variant transition-colors" title="Copy">
                  <span className="material-symbols-outlined text-sm" data-icon="content_copy">content_copy</span>
                </button>
                <button className="text-on-surface-variant hover:text-on-surface p-1 rounded hover:bg-surface-variant transition-colors" title="Download">
                  <span className="material-symbols-outlined text-sm" data-icon="download">download</span>
                </button>
              </div>
            </div>
            
            <div className="bg-[#0f172a] border border-[#1e293b] rounded-xl flex-grow flex flex-col overflow-hidden">
              <div className="flex bg-[#0f172a] border-b border-[#1e293b] px-4 py-2 items-center gap-2">
                <span className="font-code-sm text-code-sm text-outline">purchase_order_8892.json</span>
              </div>
              <div className="p-4 overflow-auto font-code-sm text-code-sm leading-relaxed text-secondary-fixed">
                <pre><code><span className="text-on-surface">{"{"}</span>
                  <br/>  <span className="text-primary">"document_type"</span>: <span className="text-tertiary">"purchase_order"</span>,
                  <br/>  <span className="text-primary">"confidence_score"</span>: <span className="text-secondary">0.98</span>,
                  <br/>  <span className="text-primary">"extracted_data"</span>: <span className="text-on-surface">{"{"}</span>
                  <br/>    <span className="text-primary">"po_number"</span>: <span className="text-tertiary">"PO-8892-XT"</span>,
                  <br/>    <span className="text-primary">"date"</span>: <span className="text-tertiary">"2024-10-24"</span>,
                  <br/>    <span className="text-primary">"vendor"</span>: <span className="text-on-surface">{"{"}</span>
                  <br/>      <span className="text-primary">"name"</span>: <span className="text-tertiary">"TechCorp Industries"</span>,
                  <br/>      <span className="text-primary">"tax_id"</span>: <span className="text-tertiary">"TC-99281-00"</span>
                  <br/>    <span className="text-on-surface">{"}"}</span>,
                  <br/>    <span className="text-primary">"line_items"</span>: <span className="text-on-surface">[</span>
                  <br/>      <span className="text-on-surface">{"{"}</span>
                  <br/>        <span className="text-primary">"description"</span>: <span className="text-tertiary">"Server Rack 42U"</span>,
                  <br/>        <span className="text-primary">"quantity"</span>: <span className="text-secondary">4</span>,
                  <br/>        <span className="text-primary">"unit_price"</span>: <span className="text-secondary">850.00</span>,
                  <br/>        <span className="text-primary">"total"</span>: <span className="text-secondary">3400.00</span>
                  <br/>      <span className="text-on-surface">{"}"}</span>
                  <br/>    <span className="text-on-surface">]</span>,
                  <br/>    <span className="text-primary">"grand_total"</span>: <span className="text-secondary">3400.00</span>
                  <br/>  <span className="text-on-surface">{"}"}</span>
                  <br/><span className="text-on-surface">{"}"}</span></code></pre>
              </div>
            </div>
          </div>
        </section>

        <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-gutter pt-8">
          <div className="bg-surface-container-low border border-outline-variant rounded-xl p-padding-card flex flex-col gap-4 hover:border-outline transition-colors">
            <div className="h-10 w-10 rounded-lg bg-surface-variant flex items-center justify-center text-primary">
              <span className="material-symbols-outlined" data-icon="computer">computer</span>
            </div>
            <div>
              <h3 className="font-body-md text-body-md font-semibold text-on-surface">Local Deployment</h3>
              <p className="font-code-sm text-code-sm text-on-surface-variant mt-1">Run fully offline on your own hardware for maximum privacy.</p>
            </div>
          </div>
          <div className="bg-surface-container-low border border-outline-variant rounded-xl p-padding-card flex flex-col gap-4 hover:border-outline transition-colors">
            <div className="h-10 w-10 rounded-lg bg-surface-variant flex items-center justify-center text-tertiary">
              <span className="material-symbols-outlined" data-icon="api">api</span>
            </div>
            <div>
              <h3 className="font-body-md text-body-md font-semibold text-on-surface">Self-hosted API</h3>
              <p className="font-code-sm text-code-sm text-on-surface-variant mt-1">Integrate our RESTful endpoints directly into your microservices.</p>
            </div>
          </div>
          <div className="bg-surface-container-low border border-outline-variant rounded-xl p-padding-card flex flex-col gap-4 hover:border-outline transition-colors">
            <div className="h-10 w-10 rounded-lg bg-surface-variant flex items-center justify-center text-secondary">
              <span className="material-symbols-outlined" data-icon="deployed_code">deployed_code</span>
            </div>
            <div>
              <h3 className="font-body-md text-body-md font-semibold text-on-surface">Docker Support</h3>
              <p className="font-code-sm text-code-sm text-on-surface-variant mt-1">Spin up instances in seconds with our optimized official images.</p>
            </div>
          </div>
          <div className="bg-surface-container-low border border-outline-variant rounded-xl p-padding-card flex flex-col gap-4 hover:border-outline transition-colors">
            <div className="h-10 w-10 rounded-lg bg-surface-variant flex items-center justify-center text-on-surface">
              <span className="material-symbols-outlined" data-icon="code">code</span>
            </div>
            <div>
              <h3 className="font-body-md text-body-md font-semibold text-on-surface">Open Source Core</h3>
              <p className="font-code-sm text-code-sm text-on-surface-variant mt-1">Built on transparent models. Extend and modify as needed.</p>
            </div>
          </div>
        </section>
      </main>
      
      <footer className="bg-surface-container-lowest border-t border-outline-variant w-full mt-auto">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:flex lg:justify-between items-center w-full px-gutter py-8 max-w-container-max mx-auto gap-gutter">
          <div className="flex items-center gap-2">
            <span className="font-headline-lg-mobile text-headline-lg-mobile font-bold text-on-surface">OCR.dev</span>
          </div>
          <div className="flex flex-wrap gap-6">
            <a className="font-label-caps text-label-caps text-on-surface-variant hover:text-on-surface transition-colors active:opacity-80" href="#">Features</a>
            <a className="font-label-caps text-label-caps text-on-surface-variant hover:text-on-surface transition-colors active:opacity-80" href="#">API Docs</a>
            <a className="font-label-caps text-label-caps text-on-surface-variant hover:text-on-surface transition-colors active:opacity-80" href="#">GitHub</a>
            <a className="font-label-caps text-label-caps text-on-surface-variant hover:text-on-surface transition-colors active:opacity-80" href="#">Privacy</a>
            <a className="font-label-caps text-label-caps text-on-surface-variant hover:text-on-surface transition-colors active:opacity-80" href="#">Terms</a>
          </div>
          <div className="font-body-md text-body-md text-on-surface-variant">
            © 2024 OCR.dev. Released under MIT License.
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
