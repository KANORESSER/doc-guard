document.getElementById("verifyBtn").addEventListener("click", function () {
    var code = document.getElementById("otpInput").value;

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/otp/verify", true);
    xhr.setRequestHeader("Content-Type", "application/json");

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4) {
            var response = JSON.parse(xhr.responseText);

            if (xhr.status === 200) {
                document.getElementById("message").innerText = "認証成功！";
            } else {
                if (response.detail === "OTP expired") {
                    document.getElementById("message").innerText = "有効期限が切れています";
                } else if (response.detail === "OTP already used") {
                    document.getElementById("message").innerText = "既に使用済みのコードです";
                } else if (response.detail === "Invalid OTP") {
                    document.getElementById("message").innerText = "認証コードが正しくありません";
                } else {
                    document.getElementById("message").innerText = "認証に失敗しました";
                }
            }
        }
    };

    xhr.send(JSON.stringify({ code: code }));
});



document.getElementById("generateBtn").addEventListener("click", function () {
    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/otp/generate", true);

    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var data = JSON.parse(xhr.responseText);

            document.getElementById("modalOtpText").innerText = data.otp;
            document.getElementById("otpModal").classList.remove("hidden");
        }
    };

    xhr.send();
});

document.getElementById("closeModalBtn").addEventListener("click", function () {
    document.getElementById("otpModal").classList.add("hidden");
});
