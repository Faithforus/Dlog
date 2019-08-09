function formatString(str, data) {
    //'a{0}ab{1}b',a,b  ==>  aaabbb
    //'a{i}ab{j}b',{i:a,j:b} ==>  aaabbb
    if (!str || data == undefined) {
        return str;
    }

    if (typeof data === "object") {
        for (var key in data) {
            if (data.hasOwnProperty(key)) {
                str = str.replace(new RegExp("\{" + key + "\}", "g"), data[key]);
            }
        }
    } else {
        var args = arguments,
            reg = new RegExp("\{([0-" + (args.length - 1) + "])\}", "g");
        return str.replace(reg, function (match, index) {
            return args[index - (-1)];
        });
    }
    return str;
};

window.addEventListener('beforeunload', (event) => {
    // Cancel the event as stated by the standard.
    event.preventDefault();
    // Chrome requires returnValue to be set.
    event.returnValue = '';
});