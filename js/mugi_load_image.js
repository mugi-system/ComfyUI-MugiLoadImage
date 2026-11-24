import { app } from "../../scripts/app.js";

// When a real file is chosen in the MugiLoadImage node's image widget
// (file picker, drag & drop upload, etc.), copy its name into the
// "original_filename" widget. Values starting with "clipspace" are the
// mask editor's temp files and must NOT overwrite the stored name:
// painting a mask rewrites the image widget to a clipspace file, and
// the whole point of this node is that the original name survives that.
app.registerExtension({
    name: "mugi.LoadImageKeepFilename",
    nodeCreated(node) {
        if (!node || node.comfyClass !== "MugiLoadImage") return;
        const widgets = node.widgets || [];
        const imageWidget = widgets.find((w) => w.name === "image");
        const nameWidget = widgets.find((w) => w.name === "original_filename");
        if (!imageWidget || !nameWidget) return;

        const remember = (value) => {
            if (typeof value !== "string" || !value) return;
            if (value.startsWith("clipspace")) return;
            if (nameWidget.value !== value) {
                nameWidget.value = value;
            }
        };

        const originalCallback = imageWidget.callback;
        imageWidget.callback = function (value, ...rest) {
            remember(value);
            if (originalCallback) {
                return originalCallback.call(this, value, ...rest);
            }
            return undefined;
        };

        // If the node was created with a real file already selected
        // (e.g. drag & drop creates the node and assigns the file),
        // capture it too, unless a name is already stored.
        if (!nameWidget.value && typeof imageWidget.value === "string") {
            remember(imageWidget.value);
        }
    },
});
