using System.Collections;
using UnityEngine;
using UnityEngine.Networking;

public class ScreenshotCapture : MonoBehaviour {
    public string shotApiUrl = 'http://127.0.0.1:5000/api/screenshot-capture';
    public IEnumerator CaptureScreenshotAndSend () {
        yield return new WaitForEndOfFrame();

        // Capture the screenshot of the scene [planet]
        RenderTexture renderTexture = new RenderTexture(Screen.width, Screen.height, 24);
        Texture2D screenshotTexture = new Texture2D(Screen.width, Screen.height, TextureFormat.RGB24, false);
        Camera.main.targetTexture = renderTexture;
        Camera.main.Render();
        RenderTexture.active = renderTexture;
        screenshotTexture.ReadPixels(new Rect(0, 0, Screen.width, Screen.height), 0, 0);
        Camera.main.targetTexture = null;
        RenderTexture.active = null;
        Destroy(renderTexture);

        byte[] screenshotBytes = screenshotTexture.EncodeToPNG();
        Destroy(screenshotTexture);

        // Send the screenshot to Flask
        UnityWebRequest request = new UnityWebRequest(shotApiUrl, UnityWebRequest.kHttpVerbPOST);
        request.SetRequestHeader("Content-Type", "image/png");
        request.uploadHandler = new UploadHandlerRaw(screenshotBytes);
        request.downloadHandler = new DownloadHandlerBuffer();

        yield return request.SendWebRequest();

        if (request.result != UnityWebRequest.Result.Success) {
            Debug.Log("Error capturing & sending the screenshot: " + request.error);
        } else {
            Debug.Log("Screenshot captured & sent succesfully. " + request)
            string response = request.downloadHandler.text;
        }
    }
}