from io import BytesIO
from datetime import datetime
import json
import pandas as pd
from models.dto.export_result import ExportResult
from models.dto.export_dto import ExportDTO
from services.logger_service import logger


class ExportService:
    def export(self, dto: ExportDTO) -> ExportResult:
        df_list = self._ensure_multiple_df(dto.data)
        base = f"export_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

        try:
            if dto.format == "excel":
                return self._to_excel(df_list, base)
            elif dto.format == "json":
                return self._to_json(df_list, base)
            elif dto.format == "csv":
                return self._to_csv(df_list, base)
            else:
                raise ValueError(f"Неподдерживаемый формат: {dto.format}")
        except Exception as e:
            raise Exception(str(e))
        
    def _ensure_df(self, data) -> pd.DataFrame:
        if isinstance(data, pd.DataFrame):
            return data

        if isinstance(data, list) and isinstance(data[0], dict):
            return pd.DataFrame(data)

        if isinstance(data, list) and isinstance(data[0], list):
            return pd.DataFrame(data)

        if isinstance(data, (int, float, str)):
            return pd.DataFrame([data])

        raise ValueError(f"Неизвестный формат данных: {type(data)}")


    def _ensure_multiple_df(self, data) -> list:
        if isinstance(data, list):
            return [self._ensure_df(d) for d in data]
        else:
            return [self._ensure_df(data)]

    def _to_excel(self, df_list: list, base: str) -> ExportResult:
        buf = BytesIO()

        with pd.ExcelWriter(buf, engine="xlsxwriter", engine_kwargs={"options": {"strings_to_urls": False}}) as w:
            sheet_name = "Data"
            all_data = pd.concat(df_list, ignore_index=True)

            all_data.to_excel(w, index=False, sheet_name=sheet_name)

            ws = w.sheets[sheet_name]
            for i, col in enumerate(all_data.columns):
                series = all_data.iloc[:, i].astype(str)
                max_len = max([len(str(col))] + [len(v) for v in series.values if v is not None])
                ws.set_column(i, i, min(max_len + 2, 60))

        buf.seek(0)
        return ExportResult(
            content=buf.read(),
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            filename=f"{base}.xlsx",
        )


    def _to_json(self, df_list: list, base: str) -> ExportResult:
        try:
            json_content = []
            for df in df_list:
                json_content.extend(df.to_dict(orient="records"))

            text = json.dumps(json_content, ensure_ascii=False, indent=2)
            return ExportResult(
                content=text.encode("utf-8"),
                mime="application/json; charset=utf-8",
                filename=f"{base}.json",
            )
        except Exception as e:
            logger.error(f"Ошибка при экспорте в JSON: {e}")
            raise ValueError(f"Ошибка при экспорте в JSON: {e}")


    def _to_csv(self, df_list: list, base: str) -> ExportResult:
        try:
            csv_content = ""

            for idx, df in enumerate(df_list):
                csv_content += df.to_csv(index=False, header=(idx == 0), sep=",", decimal=".", na_rep="", lineterminator="\n")

            return ExportResult(
                content=csv_content.encode("utf-8"),
                mime="text/csv; charset=utf-8",
                filename=f"{base}.csv",
            )
        except Exception as e:
            logger.error(f"Ошибка при экспорте в CSV: {e}")
            raise ValueError(f"Ошибка при экспорте в CSV: {e}")
