<template>
  <div class="input-zone">
    <div ref="editor" class="editor"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from "vue";
import { EditorState } from "@codemirror/state";
import { EditorView, keymap, highlightActiveLine, lineNumbers, highlightSpecialChars } from "@codemirror/view";
import { basicSetup } from "codemirror";
import { defaultKeymap, history, historyKeymap, indentWithTab } from "@codemirror/commands";
import { sql } from "@codemirror/lang-sql";
import { acceptCompletion,autocompletion, completionKeymap } from "@codemirror/autocomplete";
import { defineExpose } from "vue";

const editor = ref(null)
const editorView = ref(null)

const getSQL = () => {
  if (editorView.value) {
    return editorView.value.state.doc.toString()
  }
  return ''
}

onMounted(() => {
  if (!editor.value) return

  editorView.value = new EditorView({
    state: EditorState.create({
      doc: "",
      extensions: [
        lineNumbers(),
        highlightSpecialChars(),
        highlightActiveLine(),
        history(),
        keymap.of([
          {
            key: "Tab",
            run: (view) => {
              if (acceptCompletion(view)) {
                return true;
              }
              return indentWithTab.run(view);
            },
            preventDefault: true,
          },
          ...defaultKeymap,
          ...historyKeymap,
          ...completionKeymap
        ]),
        autocompletion(),
        EditorView.lineWrapping,
        basicSetup,
        sql()
      ],
    }),
    parent: editor.value,
  })
})

onBeforeUnmount(() => {
  if (editorView.value) {
    editorView.value.destroy();
    editorView.value = null;
  }
})

defineExpose({
  getSQL
})
</script>

<style scoped>
.input-zone {
  width: 100%;
  height: 100%;
  background-color: #f5f5f5;
  border-radius: 0.5rem;
  padding: clamp(0.75rem, 3vw, 1rem);
  box-shadow: 0 0.125rem 0.625rem rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.editor {
  flex: 1;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  font-family: 'Fira Mono', monospace;
  font-size: clamp(0.875rem, 2vw, 0.875rem);
  background-color: white;
  outline: none;
  overflow-y: auto;
  caret-color: #1890ff;
  margin-bottom: 0.625rem;
}

.send-button {
  padding: 0.5rem 1rem;
  background-color: #1890ff;
  color: white;
  border: none;
  border-radius: 0.25rem;
  cursor: pointer;
  align-self: flex-end;
}

.send-button:hover {
  background-color: #096dd9;
}

.cm-activeLine {
  background-color: #f0f8ff !important;
}
</style>