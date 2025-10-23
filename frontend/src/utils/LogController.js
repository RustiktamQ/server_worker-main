export default class LogController {
  constructor(logRef) {
    this.storage = logRef.value;
  }

  _generateLog(server, status, action, message, duration) {
    if (
      status != "loading" &&
      status != "success" &&
      status != "error" &&
      status != "info"
    ) {
      throw new Error("invalid status type");
    }

    const now = new Date();
    const time = now.toLocaleTimeString("ru-RU", { hour12: false });
    const id = Math.floor(Math.random() * 1_000_000) + 1;

    return { id, server, status, time, action, message, duration };
  }

  addLog(status, action, message, server = "-", duration = "-") {
    const log = this._generateLog(server, status, action, message, duration);
    this.storage.push(log);

    return log.id;
  }

  changeLog(id, status, action, message, duration = "-") {
    for (const log of this.storage) {
      if (log.id === id) {
        log.status = status;
        log.action = action;
        log.message = message;
        log.duration = duration + " сек";

        return true;
      }
    }

    return false;
  }
}
