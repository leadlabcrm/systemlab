import { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import mermaid from 'mermaid';
import { useParams } from 'react-router-dom';

mermaid.initialize({
  startOnLoad: false,
  theme: 'dark',
  themeVariables: {
    fontFamily: 'Inter, sans-serif',
    primaryColor: '#191919',
    primaryTextColor: '#ffffff',
    primaryBorderColor: '#212327',
    lineColor: '#ffffff',
    secondaryColor: '#0a0a0a'
  }
});

function MermaidChart({ chart }: { chart: string }) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (ref.current && chart) {
      mermaid.render(`mermaid-${Math.random().toString(36).substr(2, 9)}`, chart).then(result => {
        if (ref.current) ref.current.innerHTML = result.svg;
      }).catch(e => console.error('Mermaid render error', e));
    }
  }, [chart]);

  return <div ref={ref} className="mermaid-container" />;
}

export default function SopRenderer() {
  const { categoryId, sopId } = useParams();
  const [content, setContent] = useState('');
  const [isEditing, setIsEditing] = useState(false);

  useEffect(() => {
    if (!categoryId || !sopId) return;
    
    // Load from local storage or set default
    const storageKey = `sop_${categoryId}_${sopId}`;
    const saved = localStorage.getItem(storageKey);
    
    if (saved) {
      setContent(saved);
    } else {
      const demoContent = `# ${sopId.replace(/-/g, ' ').replace(/\\b\\w/g, c => c.toUpperCase())}

This is a demonstration of the SystemLab standard operating procedure format.

## Flowchart
\`\`\`mermaid
graph TD
  A[Start Process] --> B{Is it qualified?};
  B -- Yes --> C[Proceed to next step];
  B -- No --> D[End process];
\`\`\`

## Video Walkthrough
\`\`\`loom
https://www.loom.com/share/c0faec017b204ce4997193f211d1bb6d
\`\`\`

## Text Instructions
1. Follow the flowchart above.
2. Ensure you have reviewed the video.
3. Mark complete in your tracking tool.
`;
      setContent(demoContent);
    }
    setIsEditing(false);
  }, [categoryId, sopId]);

  const handleSave = () => {
    if (categoryId && sopId) {
      localStorage.setItem(`sop_${categoryId}_${sopId}`, content);
    }
    setIsEditing(false);
  };

  return (
    <div className="sop-content">
      <div className="sop-header">
        <div>
          <span className="sop-eyebrow">{categoryId}</span>
        </div>
        <div>
          {isEditing ? (
            <button className="btn-pill primary" onClick={handleSave}>Save Changes</button>
          ) : (
            <button className="btn-pill" onClick={() => setIsEditing(true)}>Edit SOP</button>
          )}
        </div>
      </div>

      {isEditing ? (
        <div className="editor-container">
          <textarea 
            className="editor-textarea"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            spellCheck="false"
          />
        </div>
      ) : (
        <ReactMarkdown
          className="markdown-body"
          remarkPlugins={[remarkGfm]}
          components={{
            code({node, inline, className, children, ...props}: any) {
              const match = /language-(\w+)/.exec(className || '');
              const lang = match ? match[1] : '';
              
              if (!inline && lang === 'mermaid') {
                return <MermaidChart chart={String(children).replace(/\\n$/, '')} />;
              }
              if (!inline && lang === 'loom') {
                const url = String(children).trim();
                const id = url.split('/').pop();
                return (
                  <div className="loom-container">
                    <iframe 
                      src={\`https://www.loom.com/embed/\${id}\`} 
                      frameBorder="0" 
                      allowFullScreen 
                      style={{width: '100%', height: '440px', display: 'block'}}>
                    </iframe>
                  </div>
                );
              }
              return <code className={className} {...props}>{children}</code>;
            }
          }}
        >
          {content}
        </ReactMarkdown>
      )}
    </div>
  );
}
