import { useState } from 'react';
import { uploadFile, askQuestion } from './api';

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [question, setQuestion] = useState('');
  const [loading, setLoading] = useState(false);
  const [messages, setMessages] = useState<{ role: 'user' | 'ai'; text: string; sources?: any[] }[]>([]);

  const handleUpload = async () => {
    if (!file) return alert('请先选择文件');
    try {
      setLoading(true);
      const res = await uploadFile(file);
      alert(`上传成功！切分成了 ${res.chunks_count} 个片段。`);
    } catch (err) {
      console.error(err);
      alert('上传失败，请看后端终端报错');
    } finally {
      setLoading(false);
    }
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    const userMsg = question;
    setMessages((prev) => [...prev, { role: 'user', text: userMsg }]);
    setQuestion('');
    setLoading(true);

    try {
      const res = await askQuestion(userMsg);
      setMessages((prev) => [
        ...prev,
        { role: 'ai', text: res.answer, sources: res.sources },
      ]);
    } catch (err) {
      console.error(err);
      setMessages((prev) => [...prev, { role: 'ai', text: '请求出错了，请看后端终端。' }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>个人知识库</h1>

      <div style={{ border: '1px solid #ccc', padding: '15px', marginBottom: '20px', borderRadius: '8px' }}>
        <h3>1. 上传资料 (.md)</h3>
        <input type="file" accept=".md" onChange={(e) => setFile(e.target.files?.[0] || null)} />
        <button onClick={handleUpload} disabled={loading || !file} style={{ marginLeft: '10px' }}>
          上传
        </button>
      </div>

      <div style={{ border: '1px solid #ccc', padding: '15px', borderRadius: '8px', minHeight: '300px', display: 'flex', flexDirection: 'column' }}>
        <h3>2. 提问</h3>
        <div style={{ flex: 1, overflowY: 'auto', marginBottom: '10px' }}>
          {messages.map((msg, i) => (
            <div key={i} style={{ marginBottom: '15px', textAlign: msg.role === 'user' ? 'right' : 'left' }}>
              <div style={{
                display: 'inline-block',
                padding: '10px',
                borderRadius: '8px',
                backgroundColor: msg.role === 'user' ? '#d1e7dd' : '#f8d7da',
                maxWidth: '80%',
                textAlign: 'left'
              }}>
                <div style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</div>
                {msg.sources && msg.sources.length > 0 && (
                  <div style={{ marginTop: '10px', fontSize: '12px', color: '#555', borderTop: '1px dashed #aaa', paddingTop: '5px' }}>
                    <strong>参考来源：</strong>
                    {msg.sources.map((s, idx) => (
                      <div key={idx} style={{ marginTop: '5px', backgroundColor: '#fff', padding: '5px', borderRadius: '4px' }}>
                        [{idx + 1}] {s.content.slice(0, 50)}...
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
        <div style={{ display: 'flex' }}>
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            placeholder="输入你的问题..."
            style={{ flex: 1, padding: '8px', marginRight: '10px' }}
          />
          <button onClick={handleAsk} disabled={loading} style={{ padding: '8px 15px' }}>
            发送
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;