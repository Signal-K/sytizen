using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Networking;

public class SendTicNumerals : MonoBehaviour {
    public void SendRequest(string ticNumerals) {
        StartCoroutine(PostRequest("http://127.0.0.1:5000/send_tic_numerals", ticNumerals));
    }

    IEnumerator PostRequest(string uri, string ticNumerals) {
        WWWForm form = new WWWForm();
        form.AddField("tic_numerals", ticNumerals);

        UnityWebRequest uwr = UnityWebRequest.Post(uri, form);
        yield return uwr.SendWebRequest();

        if (uwr.isNetworkError) {
            Debug.Log("Error While Sending: " + uwr.error);
        }
        else {
            Debug.Log("Received: " + uwr.downloadHandler.text);
            // Process the response from Flask as needed
        }
    }
}