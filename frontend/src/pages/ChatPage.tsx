import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  MessageCircle,
  Send,
  FileText,
  ChevronRight,
  Sparkles,
  Bot,
  User,
  Image as ImageIcon,
  Globe
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Textarea } from '@/components/ui/textarea';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Badge } from '@/components/ui/badge';
import api from '../api/client';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  source?: string;
  image?: string;
}

const initialMessagesCN: Message[] = [
  {
    id: '1',
    role: 'assistant',
    content: '你好！我已经学习了你上传的《高中数学必修一》。当前我们位于 **第一章：集合与函数概念**。\n\n你可以问我：\n• "什么是函数的定义域？"\n• "帮我总结单调性的判定方法"\n• "上传一道题目帮我解析"',
  },
  {
    id: '2',
    role: 'user',
    content: '函数 f(x) = √(x-1) 的定义域是什么？',
  },
  {
    id: '3',
    role: 'assistant',
    content: '**知识点：定义域**\n**页码：P23**\n\n要求函数 f(x) = √(x-1) 的定义域，需要考虑平方根的被开方数必须非负。\n\n**解题步骤：**\n1. 被开方数 x - 1 ≥ 0\n2. 解得 x ≥ 1\n\n∴ **定义域为 [1, +∞)**',
    source: '基于《高中数学必修一》回答',
  },
];

const initialMessagesEN: Message[] = [
  {
    id: '1',
    role: 'assistant',
    content: 'Hello! I have studied the "High School Mathematics Compulsory 1" you uploaded. We are currently in **Chapter 1: Sets and Function Concepts**.\n\nYou can ask me:\n• "What is the domain of a function?"\n• "Help me summarize the methods for determining monotonicity"\n• "Upload a problem for me to analyze"',
  },
  {
    id: '2',
    role: 'user',
    content: 'What is the domain of the function f(x) = √(x-1)?',
  },
  {
    id: '3',
    role: 'assistant',
    content: '**Knowledge Point: Domain**\n**Page: P23**\n\nTo find the domain of f(x) = √(x-1), we need to consider that the expression under the square root must be non-negative.\n\n**Solution Steps:**\n1. The radicand x - 1 ≥ 0\n2. Solving gives x ≥ 1\n\n∴ **The domain is [1, +∞)**',
    source: 'Based on "High School Mathematics Compulsory 1"',
  },
];

const translations = {
  cn: {
    knowledgeBase: '知识库',
    manageMaterials: '管理你的学习资料',
    viewDocuments: '查看我的文档',
    textbook: '《高中数学必修一》',
    footer: 'Everything up to you',
    aiChat: '智能问答',
    aiOnline: 'AI 助手在线',
    placeholder: '输入你的问题，Enter 发送，Shift+Enter 换行',
    uploadImage: '上传图片',
    disclaimer: 'AI 回答基于《高中数学必修一》教材内容',
    deepseekOnline: 'DeepSeek 在线',
  },
  en: {
    knowledgeBase: 'Knowledge Base',
    manageMaterials: 'Manage your learning materials',
    viewDocuments: 'View My Documents',
    textbook: '"High School Math Compulsory 1"',
    footer: 'Everything up to you',
    aiChat: 'AI Chat',
    aiOnline: 'AI Assistant Online',
    placeholder: 'Type your question, Enter to send, Shift+Enter for new line',
    uploadImage: 'Upload Image',
    disclaimer: 'AI responses based on "High School Mathematics Compulsory 1"',
    deepseekOnline: 'DeepSeek Online',
  }
};

function ChatPage() {
  const [language, setLanguage] = useState<'cn' | 'en'>('cn');
  const [messages, setMessages] = useState<Message[]>(initialMessagesCN);
  const [inputValue, setInputValue] = useState('');
  const [uploadedImage, setUploadedImage] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [currentDocument, setCurrentDocument] = useState<string>('4ec6fb98-1bef-476e-bcba-bda5394c059f'); // Default document
  const fileInputRef = useRef<HTMLInputElement>(null);
  const scrollRef = useRef<HTMLDivElement>(null);

  const t = translations[language];

  useEffect(() => {
    setMessages(language === 'cn' ? initialMessagesCN : initialMessagesEN);
  }, [language]);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'cn' ? 'en' : 'cn');
  };

  const handleImageUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        setUploadedImage(event.target?.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleSend = async () => {
    if (!inputValue.trim() && !uploadedImage) return;

    const newMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: inputValue,
      image: uploadedImage || undefined,
    };

    setMessages([...messages, newMessage]);
    setInputValue('');
    setUploadedImage(null);
    setIsLoading(true);

    try {
      // Call the real API
      const response = await api.post('/qa/ask', {
        question: inputValue,
        document_id: currentDocument,
        top_k: 3,
      });

      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.data.answer || '抱歉，我无法回答这个问题。',
        source: response.data.provider ? `基于 ${response.data.provider} 回答` : '基于文档回答',
      };
      setMessages(prev => [...prev, aiResponse]);
    } catch (error: any) {
      // Fallback to mock response on error
      const errorMessage = error.response?.data?.detail || '服务暂时不可用';
      const aiResponse: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: language === 'cn'
          ? `抱歉，发生了错误：${errorMessage}`
          : `Sorry, an error occurred: ${errorMessage}`,
        source: 'Error',
      };
      setMessages(prev => [...prev, aiResponse]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div className="h-screen flex bg-gradient-to-br from-slate-50 to-slate-100 overflow-hidden">
      {/* Left Sidebar - Knowledge Base */}
      <aside className="w-72 bg-white border-r border-slate-200 flex flex-col shadow-sm">
        {/* Logo */}
        <div className="p-5 border-b border-slate-100">
          <div className="flex items-center gap-2">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
              <Sparkles className="w-5 h-5 text-white" />
            </div>
            <div>
              <h1 className="font-bold text-slate-800 text-lg">StudyFlow AI</h1>
              <p className="text-xs text-slate-500">{t.deepseekOnline}</p>
            </div>
          </div>
        </div>

        {/* Knowledge Base Section */}
        <div className="p-5 flex-1">
          <Link to="/knowledge-base" className="block">
            <div className="flex items-center gap-2 mb-4 cursor-pointer hover:opacity-80 transition-opacity">
              <BookOpen className="w-4 h-4 text-indigo-600" />
              <h2 className="font-semibold text-slate-700">{t.knowledgeBase}</h2>
            </div>
          </Link>
          
          <p className="text-sm text-slate-500 mb-4">{t.manageMaterials}</p>
          
          <Link to="/knowledge-base">
            <button className="w-full flex items-center gap-3 p-3 rounded-xl bg-indigo-50 border border-indigo-100 hover:bg-indigo-100 transition-colors">
              <FileText className="w-5 h-5 text-indigo-600" />
              <div className="text-left flex-1">
                <p className="text-sm font-medium text-slate-700">{t.viewDocuments}</p>
                <p className="text-xs text-slate-500">{t.textbook}</p>
              </div>
              <ChevronRight className="w-4 h-4 text-slate-400" />
            </button>
          </Link>
        </div>

        {/* Bottom Info */}
        <div className="p-4 border-t border-slate-100">
          <p className="text-xs text-slate-400 text-center">
            {t.footer}
          </p>
        </div>
      </aside>

      {/* Main Chat Area */}
      <main className="flex-1 flex flex-col">
        {/* Header */}
        <header className="h-16 bg-white/80 backdrop-blur-sm border-b border-slate-200 flex items-center justify-between px-6">
          <div className="flex items-center gap-2">
            <MessageCircle className="w-5 h-5 text-indigo-600" />
            <h2 className="font-semibold text-slate-700">{t.aiChat}</h2>
          </div>
          <div className="flex items-center gap-3">
            {/* Language Toggle */}
            <Button
              variant="outline"
              size="sm"
              onClick={toggleLanguage}
              className="flex items-center gap-2 text-slate-600 border-slate-300 hover:bg-slate-50"
            >
              <Globe className="w-4 h-4" />
              <span className="font-medium">{language === 'cn' ? '中文' : 'EN'}</span>
            </Button>
            <Badge variant="outline" className="text-slate-500 border-slate-300">
              <Bot className="w-3 h-3 mr-1" />
              {t.aiOnline}
            </Badge>
          </div>
        </header>

        {/* Chat Messages */}
        <ScrollArea className="flex-1 p-6" ref={scrollRef}>
          <div className="max-w-3xl mx-auto space-y-6">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex gap-4 ${
                  message.role === 'user' ? 'flex-row-reverse' : ''
                }`}
              >
                {/* Avatar */}
                <div
                  className={`w-10 h-10 rounded-full flex-shrink-0 flex items-center justify-center ${
                    message.role === 'user'
                      ? 'bg-indigo-600'
                      : 'bg-gradient-to-br from-violet-500 to-indigo-600'
                  }`}
                >
                  {message.role === 'user' ? (
                    <User className="w-5 h-5 text-white" />
                  ) : (
                    <Bot className="w-5 h-5 text-white" />
                  )}
                </div>

                {/* Message Content */}
                <div
                  className={`max-w-[calc(100%-4rem)] ${
                    message.role === 'user' ? 'text-right' : ''
                  }`}
                >
                  {/* Image if exists */}
                  {message.image && (
                    <div className={`mb-2 ${message.role === 'user' ? 'text-right' : ''}`}>
                      <img 
                        src={message.image} 
                        alt="Uploaded" 
                        className="max-w-[200px] max-h-[200px] rounded-xl border border-slate-200 shadow-sm inline-block"
                      />
                    </div>
                  )}
                  
                  <div
                    className={`inline-block px-5 py-3 rounded-2xl text-left ${
                      message.role === 'user'
                        ? 'bg-indigo-600 text-white'
                        : 'bg-white border border-slate-200 text-slate-700 shadow-sm'
                    }`}
                  >
                    <div className="whitespace-pre-wrap leading-relaxed">
                      {message.content.split('**').map((part, i) => 
                        i % 2 === 1 ? (
                          <strong key={i} className={message.role === 'user' ? 'text-indigo-100' : 'text-indigo-700'}>
                            {part}
                          </strong>
                        ) : (
                          part
                        )
                      )}
                    </div>
                  </div>
                  
                  {/* Source */}
                  {message.source && (
                    <p className="mt-2 text-xs text-slate-400 flex items-center gap-1 justify-start">
                      <BookOpen className="w-3 h-3" />
                      {message.source}
                    </p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </ScrollArea>

        {/* Input Area */}
        <div className="p-6 bg-white border-t border-slate-200">
          <div className="max-w-3xl mx-auto">
            {/* Image Preview */}
            {uploadedImage && (
              <div className="mb-3 relative inline-block">
                <img 
                  src={uploadedImage} 
                  alt="Preview" 
                  className="max-h-[80px] rounded-lg border border-slate-200"
                />
                <button
                  onClick={() => setUploadedImage(null)}
                  className="absolute -top-2 -right-2 w-5 h-5 bg-red-500 text-white rounded-full text-xs flex items-center justify-center hover:bg-red-600"
                >
                  ×
                </button>
              </div>
            )}
            
            <div className="relative">
              <Textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={handleKeyDown}
                placeholder={t.placeholder}
                className="min-h-[80px] pr-28 resize-none bg-slate-50 border-slate-200 focus:bg-white focus:border-indigo-300 focus:ring-indigo-200 rounded-xl"
              />
              
              {/* Action Buttons */}
              <div className="absolute bottom-3 right-3 flex items-center gap-2">
                {/* Image Upload Button */}
                <input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleImageUpload}
                  accept="image/*"
                  className="hidden"
                />
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => fileInputRef.current?.click()}
                  className="w-9 h-9 p-0 rounded-lg text-slate-500 hover:text-indigo-600 hover:bg-indigo-50"
                  title={t.uploadImage}
                >
                  <ImageIcon className="w-5 h-5" />
                </Button>
                
                {/* Send Button */}
                <Button
                  onClick={handleSend}
                  disabled={(!inputValue.trim() && !uploadedImage) || isLoading}
                  className="w-10 h-10 p-0 rounded-lg bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50"
                >
                  <Send className="w-4 h-4" />
                </Button>
              </div>
            </div>
            <p className="mt-2 text-xs text-slate-400 text-center">
              {t.disclaimer}
            </p>
          </div>
        </div>
      </main>
    </div>
  );
}

export default ChatPage;
