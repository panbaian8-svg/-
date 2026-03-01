import { useState, useRef, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  BookOpen,
  Search,
  Upload,
  FileText,
  ChevronLeft,
  Sparkles,
  X,
  AlertCircle,
  File,
  MoreVertical,
  Trash2,
  Download,
  Globe
} from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { Alert, AlertDescription } from '@/components/ui/alert';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import api from '../api/client';

interface Document {
  id: string;
  name: string;
  size: string;
  uploadDate: string;
}

const mockDocuments: Document[] = [
  { id: '1', name: 'High School Math Compulsory 1.docx', size: '2.3 MB', uploadDate: '2024-03-01' },
  { id: '2', name: 'Function Exercises.docx', size: '1.1 MB', uploadDate: '2024-02-28' },
  { id: '3', name: 'Sets and Logic.docx', size: '856 KB', uploadDate: '2024-02-25' },
];

const translations = {
  cn: {
    back: '返回',
    title: '我的知识库',
    importMaterials: '导入学习资料',
    alertMessage: '仅支持Word和PDF格式文件（.doc, .docx, .pdf）',
    searchDocuments: '搜索文档',
    searchPlaceholder: '搜索文档名称...',
    uploadedDocuments: '已上传的资料',
    filesCount: '个文件',
    noDocuments: '暂无文档',
    noDocumentsHint: '点击右上角"导入学习资料"添加文件',
    download: '下载',
    delete: '删除',
    cancel: '取消',
    confirmImport: '确认导入',
    selectFile: '点击选择文件',
    dragFile: '或将文件拖拽到此处',
    error: '加载文档失败',
    uploadError: '上传失败',
    deleteError: '删除失败',
  },
  en: {
    back: 'Back',
    title: 'My Knowledge Base',
    importMaterials: 'Import Materials',
    alertMessage: 'Only Word and PDF files are supported (.doc, .docx, .pdf)',
    searchDocuments: 'Search Documents',
    searchPlaceholder: 'Search documents...',
    uploadedDocuments: 'Uploaded Documents',
    filesCount: 'files',
    noDocuments: 'No documents yet',
    noDocumentsHint: 'Click "Import Materials" to add files',
    download: 'Download',
    delete: 'Delete',
    cancel: 'Cancel',
    confirmImport: 'Confirm Import',
    selectFile: 'Click to select file',
    dragFile: 'or drag and drop here',
    error: 'Failed to load documents',
    uploadError: 'Upload failed',
    deleteError: 'Delete failed',
  }
};

function KnowledgeBasePage() {
  const [language, setLanguage] = useState<'cn' | 'en'>('en');
  const [documents, setDocuments] = useState<Document[]>([]);
  const [searchQuery, setSearchQuery] = useState('');
  const [isUploadDialogOpen, setIsUploadDialogOpen] = useState(false);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const t = translations[language];

  const toggleLanguage = () => {
    setLanguage(prev => prev === 'cn' ? 'en' : 'cn');
  };

  // Fetch documents from API
  useEffect(() => {
    const fetchDocuments = async () => {
      setIsLoading(true);
      try {
        const response = await api.get('/documents');
        // Transform API response to Document format
        const docs = response.data.map((doc: any) => ({
          id: doc.id,
          name: doc.title || doc.file_name || 'Unknown',
          size: (doc.size || doc.file_size) ? `${((doc.size || doc.file_size) / 1024 / 1024).toFixed(1)} MB` : '0 MB',
          uploadDate: doc.upload_date ? new Date(doc.upload_date).toISOString().split('T')[0] : new Date().toISOString().split('T')[0],
        }));
        setDocuments(docs);
      } catch (err: any) {
        console.error('Failed to fetch documents:', err);
        setError(t.error);
        // Fallback to mock data
        setDocuments(mockDocuments);
      } finally {
        setIsLoading(false);
      }
    };
    fetchDocuments();
  }, []);

  const filteredDocuments = documents.filter(doc =>
    doc.name.toLowerCase().includes(searchQuery.toLowerCase())
  );

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      // Check if it's a Word document
      if (file.name.endsWith('.doc') || file.name.endsWith('.docx') || file.name.endsWith('.pdf')) {
        setUploadedFile(file);
      } else {
        alert(t.alertMessage);
      }
    }
  };

  const handleUpload = async () => {
    if (!uploadedFile) return;

    setIsLoading(true);
    const formData = new FormData();
    formData.append('file', uploadedFile);

    try {
      const response = await api.post('/documents/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      const newDoc: Document = {
        id: response.data.document_id,
        name: uploadedFile.name,
        size: `${(uploadedFile.size / 1024 / 1024).toFixed(1)} MB`,
        uploadDate: new Date().toISOString().split('T')[0],
      };
      setDocuments([newDoc, ...documents]);
      setUploadedFile(null);
      setIsUploadDialogOpen(false);
    } catch (err: any) {
      console.error('Upload failed:', err);
      alert(err.response?.data?.detail || t.uploadError);
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await api.delete(`/documents/${id}`);
      setDocuments(documents.filter(doc => doc.id !== id));
    } catch (err: any) {
      console.error('Delete failed:', err);
      alert(err.response?.data?.detail || t.deleteError);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100">
      {/* Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-4">
            <Link to="/" className="flex items-center gap-2 text-slate-600 hover:text-indigo-600 transition-colors">
              <ChevronLeft className="w-5 h-5" />
              <span className="text-sm font-medium">{t.back}</span>
            </Link>
            <div className="w-px h-6 bg-slate-200" />
            <div className="flex items-center gap-2">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-violet-600 flex items-center justify-center">
                <Sparkles className="w-4 h-4 text-white" />
              </div>
              <h1 className="font-bold text-slate-800">{t.title}</h1>
            </div>
          </div>
          
          {/* Language Toggle & Import Button */}
          <div className="flex items-center gap-3">
            <Button
              variant="outline"
              size="sm"
              onClick={toggleLanguage}
              className="flex items-center gap-2 text-slate-600 border-slate-300 hover:bg-slate-50"
            >
              <Globe className="w-4 h-4" />
              <span className="font-medium">{language === 'cn' ? '中文' : 'EN'}</span>
            </Button>
            <Button
              onClick={() => setIsUploadDialogOpen(true)}
              className="bg-indigo-600 hover:bg-indigo-700"
            >
              <Upload className="w-4 h-4 mr-2" />
              {t.importMaterials}
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Alert */}
        <Alert className="mb-6 bg-amber-50 border-amber-200">
          <AlertCircle className="w-4 h-4 text-amber-600" />
          <AlertDescription className="text-amber-700">
            {t.alertMessage}
          </AlertDescription>
        </Alert>

        {/* Search Section */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-slate-700 mb-4 flex items-center gap-2">
            <Search className="w-5 h-5 text-indigo-600" />
            {t.searchDocuments}
          </h2>
          <div className="relative max-w-xl">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <Input
              type="text"
              placeholder={t.searchPlaceholder}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10 h-12 bg-white border-slate-200 rounded-xl"
            />
          </div>
        </div>

        {/* Documents Section */}
        <div>
          <h2 className="text-lg font-semibold text-slate-700 mb-4 flex items-center gap-2">
            <BookOpen className="w-5 h-5 text-indigo-600" />
            {t.uploadedDocuments}
            <span className="text-sm font-normal text-slate-500 ml-2">
              ({filteredDocuments.length} {t.filesCount})
            </span>
          </h2>

          {filteredDocuments.length === 0 ? (
            <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 border-dashed">
              <FileText className="w-16 h-16 text-slate-300 mx-auto mb-4" />
              <p className="text-slate-500 mb-2">{t.noDocuments}</p>
              <p className="text-sm text-slate-400">{t.noDocumentsHint}</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
              {filteredDocuments.map((doc, index) => (
                <div
                  key={doc.id || `doc-${index}`}
                  className="group bg-white rounded-xl border border-slate-200 p-4 hover:shadow-md hover:border-indigo-200 transition-all"
                >
                  {/* File Cover */}
                  <div className="aspect-[3/4] bg-gradient-to-br from-indigo-50 to-violet-50 rounded-lg mb-4 flex items-center justify-center relative overflow-hidden">
                    <div className="absolute inset-0 bg-white/50" />
                    <FileText className="w-16 h-16 text-indigo-300 relative z-10" />
                    
                    {/* Actions */}
                    <div className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity z-20">
                      <DropdownMenu>
                        <DropdownMenuTrigger asChild>
                          <Button variant="ghost" size="sm" className="w-8 h-8 p-0 bg-white/80 hover:bg-white">
                            <MoreVertical className="w-4 h-4 text-slate-600" />
                          </Button>
                        </DropdownMenuTrigger>
                        <DropdownMenuContent align="end">
                          <DropdownMenuItem className="cursor-pointer">
                            <Download className="w-4 h-4 mr-2" />
                            {t.download}
                          </DropdownMenuItem>
                          <DropdownMenuItem
                            className="cursor-pointer text-red-600"
                            onClick={() => handleDelete(doc.id)}
                          >
                            <Trash2 className="w-4 h-4 mr-2" />
                            {t.delete}
                          </DropdownMenuItem>
                        </DropdownMenuContent>
                      </DropdownMenu>
                    </div>
                  </div>

                  {/* File Info */}
                  <div>
                    <h3 className="font-medium text-slate-700 truncate" title={doc.name}>
                      {doc.name}
                    </h3>
                    <div className="flex items-center justify-between mt-2 text-sm text-slate-500">
                      <span>{doc.size}</span>
                      <span>{doc.uploadDate}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Upload Dialog */}
      <Dialog open={isUploadDialogOpen} onOpenChange={setIsUploadDialogOpen}>
        <DialogContent className="sm:max-w-md">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2">
              <Upload className="w-5 h-5 text-indigo-600" />
              {t.importMaterials}
            </DialogTitle>
          </DialogHeader>
          
          <div className="space-y-4">
            {/* Warning */}
            <Alert className="bg-amber-50 border-amber-200">
              <AlertCircle className="w-4 h-4 text-amber-600" />
              <AlertDescription className="text-amber-700">
                {t.alertMessage}
              </AlertDescription>
            </Alert>

            {/* Upload Area */}
            <div
              onClick={() => fileInputRef.current?.click()}
              className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-colors ${
                uploadedFile 
                  ? 'border-indigo-300 bg-indigo-50' 
                  : 'border-slate-300 hover:border-indigo-300 hover:bg-slate-50'
              }`}
            >
              <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileSelect}
                accept=".doc,.docx,.pdf"
                className="hidden"
              />
              
              {uploadedFile ? (
                <div className="flex items-center justify-center gap-3">
                  <File className="w-8 h-8 text-indigo-600" />
                  <div className="text-left">
                    <p className="font-medium text-slate-700">{uploadedFile.name}</p>
                    <p className="text-sm text-slate-500">
                      {(uploadedFile.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      setUploadedFile(null);
                    }}
                    className="ml-2 w-6 h-6 bg-slate-200 hover:bg-slate-300 rounded-full flex items-center justify-center"
                  >
                    <X className="w-3 h-3" />
                  </button>
                </div>
              ) : (
                <>
                  <Upload className="w-12 h-12 text-slate-400 mx-auto mb-3" />
                  <p className="text-slate-600 font-medium">{t.selectFile}</p>
                  <p className="text-sm text-slate-400 mt-1">{t.dragFile}</p>
                </>
              )}
            </div>

            {/* Buttons */}
            <div className="flex gap-3">
              <Button
                variant="outline"
                className="flex-1"
                onClick={() => {
                  setIsUploadDialogOpen(false);
                  setUploadedFile(null);
                }}
              >
                {t.cancel}
              </Button>
              <Button
                className="flex-1 bg-indigo-600 hover:bg-indigo-700"
                disabled={!uploadedFile}
                onClick={handleUpload}
              >
                {t.confirmImport}
              </Button>
            </div>
          </div>
        </DialogContent>
      </Dialog>
    </div>
  );
}

export default KnowledgeBasePage;
