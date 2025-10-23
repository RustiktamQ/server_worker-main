import axios from "axios"
import config from "@/config"

export default class ApiController {
    async getServers() {
        try {
            const res = await axios.get(`${config.FULL_HOST}/servers`)
            return res.data
        } catch (e) {
            console.error(e)
        }
    }

    async query(query, selected_server) {
        try {
            const res = await axios.post(`${config.FULL_HOST}/execute`, {
                query,
                selected_server
            });
            return res.data
        } catch (e) {
            console.error(e)
        }
    }

    async import(file, tableName, schemaName, serverId) {
        try {
            const formData = new FormData()
            formData.append('upload_file', file)
            formData.append('table_name', tableName)
            formData.append('schema_name', schemaName)
            formData.append('server_id', serverId)

            const res = await axios.post(`${config.FULL_HOST}/import`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            return res.data;
        } catch (e) {
            console.error(e);
            throw e;
        }
    }

    async export(data, format) {
        try {
            const res = await axios.post(`${config.FULL_HOST}/export`, {
                data, format
            }, {
                responseType: 'blob'
            });

            return res;
        } catch (e) {
            console.error(e);
        }
    }

    async previewImportFile(file) {
        try {
            const formData = new FormData();
            formData.append('file', file);
            const res = await axios.post(`${config.FULL_HOST}/import/preview`, formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
            });
            return res.data;
        } catch (e) {
            console.error(e);
            throw e;
        }
    }
}