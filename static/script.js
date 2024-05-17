document.addEventListener("DOMContentLoaded", () => {
    setTimeout(() => {
        if (document.querySelector(".flashed_msgs") != undefined) {
            document.querySelector(".flashed_msgs").remove();
        }
    }, 3000);
});
const goToHome = () => {
    location.href="/";
}
const deleteFeedback = async(feedbackId) => {
    post_response = await fetch(`/feedback/${feedbackId}/delete`, {method:
    "POST"}).then(response => response);
    console.log(post_response)
    if (post_response.status == 200) {
        //location.href=post_response.url;
    }
}
