import NXOpen
import NXOpen.Annotations
import NXOpen.Drawings
import os

def select_image_file():
    """Windows dosya seçim diyaloğu ile resim dosyası seçme"""
    try:
        import win32ui
        import win32con
        
        dlg = win32ui.CreateFileDialog(
            1,  # 1 = Open File Dialog
            None,  # Dosya uzantısı filtresi
            None,  # Başlangıç dizini
            win32con.OFN_HIDEREADONLY | win32con.OFN_OVERWRITEPROMPT,
            "Resim Dosyaları|*.png;*.jpg;*.jpeg;*.bmp;*.tiff|Tüm Dosyalar|*.*||"
        )
        
        if dlg.DoModal() == win32con.IDOK:
            return dlg.GetPathName()
        else:
            return None
            
    except ImportError:
        # win32ui modülü yoksa basit bir konsol girdisi kullan
        print("Lütfen resim dosyasının tam yolunu girin:")
        file_path = input()
        if os.path.isfile(file_path):
            return file_path
        else:
            print("Dosya bulunamadı!")
            return None

def insert_image(image_path, position=None, height=100.0):
    """Seçilen resmi NX çizim sayfasına ekle"""
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    
    # Çizim sayfası kontrolü
    if workPart.DrawingSheets is None or workPart.DrawingSheets.CurrentDrawingSheet is None:
        print("Lütfen önce bir çizim sayfası açın!")
        return False
    
    drawingSheet = workPart.DrawingSheets.CurrentDrawingSheet
    
    # Varsayılan konum (sayfanın merkezi)
    if position is None:
        position = NXOpen.Point3d(0.0, 0.0, 0.0)
    
    try:
        # AnnotationManager'ı al
        annotationManager = workPart.Annotations.NewAnnotationManager()
        
        # Resim oluşturucuyu başlat
        image_builder = workPart.Annotations.CreateImageAnnotationBuilder(annotationManager)
        
        # Resim dosyasını ayarla
        image_builder.ImageFile = image_path
        
        # Konumu ayarla
        image_builder.Origin.SetValue(None, position)
        
        # Yüksekliği ayarla (genişlik otomatik olarak orantılanır)
        image_builder.Height = height
        
        # Resmi oluştur
        image_annotation = image_builder.Commit()
        
        # Builder'ı temizle
        image_builder.Destroy()
        
        print(f"Resim başarıyla eklendi: {os.path.basename(image_path)}")
        return True
        
    except Exception as ex:
        print(f"Hata oluştu: {str(ex)}")
        return False

def main():
    print("=== NX Resim Ekleme Makrosu ===")
    
    # Resim dosyasını seç
    image_path = select_image_file()
    
    if image_path is None:
        print("Resim dosyası seçilmedi!")
        return
    
    # Resmi ekle
    insert_image(image_path)

if __name__ == '__main__':
    main()
