using UnityEngine;
using UnityEngine.UI;
using System.Collections;

public class APICaller : MonoBehaviour
{
    public InputField ticInputField;
    public Text resultText;

    private string baseUrl = "http://";

    public void CallAPI()
    {
        StartCoroutine(PostRequest());
    }

    private IEnumerator PostRequest()
    {
        string ticId = ticInputField.text;

        // Create a JSON object to send as the request body
        JSONObject jsonObject = new JSONObject();
        jsonObject.AddField("tic_id", ticId);

        // Create the request
        byte[] postData = System.Text.Encoding.UTF8.GetBytes(jsonObject.ToString());
        string url = baseUrl + "api/query";
        WWW www = new WWW(url, postData, new Hashtable());

        // Wait for the response
        yield return www;

        if (string.IsNullOrEmpty(www.error))
        {
            // Parse the response JSON
            JSONObject responseJson = new JSONObject(www.text);
            string medianFlux = responseJson.GetField("median_flux").str;
            string numTrees = responseJson.GetField("num_trees").str;
            string habitability = responseJson.GetField("habitability").str;
            string lifeType = responseJson.GetField("life_type").str;
            string resourceType = responseJson.GetField("resource_type").str;

            // Display the results in the Unity scene
            resultText.text = "Median Flux: " + medianFlux + "\n" +
                              "Number of Trees: " + numTrees + "\n" +
                              "Habitability: " + habitability + "\n" +
                              "Life Type: " + lifeType + "\n" +
                              "Resource Type: " + resourceType;
        }
        else
        {
            Debug.LogError("API call error: " + www.error);
        }
    }
}
