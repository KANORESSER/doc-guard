// OTP発行
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


// モーダル閉じる
document.getElementById("closeModalBtn").addEventListener("click", function () {
    document.getElementById("otpModal").classList.add("hidden");
});


// 認証
document.addEventListener("DOMContentLoaded", function () {

    const verifyBtn = document.getElementById("verifyBtn");
    const otpInput = document.getElementById("otpInput");
    const message = document.getElementById("message");

    verifyBtn.addEventListener("click", async function () {

        message.innerText = "";

        const code = otpInput.value.trim();

        if (!code) {
            message.innerText = "認証コードを入力してください";
            return;
        }

        try {
            const response = await fetch("/otp/verify", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ code: code })
            });

            if (response.ok) {
                // 成功したら遷移
                window.location.href = "/secret";
            } else {
                const data = await response.json();

                if (data.detail === "OTP expired") {
                    message.innerText = "有効期限が切れています";
                } else if (data.detail === "OTP already used") {
                    message.innerText = "既に使用済みのコードです";
                } else {
                    message.innerText = "認証コードが正しくありません";
                }
            }

        } catch (error) {
            message.innerText = "通信エラーが発生しました";
            console.error(error);
        }
    });

});
