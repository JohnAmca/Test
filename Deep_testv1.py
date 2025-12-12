def create_table_on_drawing(self, selected_points, origin, orientation):
    try:
        work_part = self.theSession.Parts.Work

        # --- 1) Drafting table oluşturmak için table builder aç ---
        table_builder = work_part.Annotations.TableBuilder()

        # Tablo başlıkları
        header = ["No", "X", "Y", "Z"]
        table_builder.NumberOfColumns = 4
        table_builder.NumberOfRows = len(selected_points) + 1  # 1 sıra başlık için

        # Başlıkları yaz
        table_builder.SetCellText(0, 0, header[0])
        table_builder.SetCellText(0, 1, header[1])
        table_builder.SetCellText(0, 2, header[2])
        table_builder.SetCellText(0, 3, header[3])

        # --- 2) Noktaları tabloya yaz ---
        for i, point in enumerate(selected_points, start=1):
            pt = self.transform_point(point.Coordinates, origin, orientation)

            table_builder.SetCellText(i, 0, str(i))
            table_builder.SetCellText(i, 1, f"{pt.X:.3f}")
            table_builder.SetCellText(i, 2, f"{pt.Y:.3f}")
            table_builder.SetCellText(i, 3, f"{pt.Z:.3f}")

        # --- 3) Tabloyu çizime yerleştir ---
        # Orijin noktası (sheet üzerinde uygun bir yere koy)
        origin_pt = NXOpen.Point3d(50.0, 50.0, 0.0)
        table_builder.Origin = origin_pt

        # Tabloyu oluştur
        table_feature = table_builder.Commit()

        table_builder.Destroy()

        self.theUI.NXMessageBox.Show("Bilgi", NXOpen.NXMessageBox.DialogType.Information,
                                     "Tablo çizime başarıyla eklendi.")

    except Exception as ex:
        self.theUI.NXMessageBox.Show("Hata", NXOpen.NXMessageBox.DialogType.Error, str(ex))
