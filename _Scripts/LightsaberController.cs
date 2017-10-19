using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class LightsaberController : MonoBehaviour {

    private SteamVR_TrackedObject trackedObj;
    private GameObject lightsaber;
    public GameObject lightsaberPrefab;

    //[SerializeField] private GameObject leftController;
    //[SerializeField] private GameObject rightController;

    //int rightIndex;
    //int leftIndex;
    //SteamVR_Controller.Device rightDevice;
    //SteamVR_Controller.Device leftDevice;

    [SerializeField]
    private UDP UDPScript;
    public GameObject network;

    private SteamVR_Controller.Device Controller
    {
        get { return SteamVR_Controller.Input((int)trackedObj.index); }
    }

    private void Awake()
    {
        trackedObj = GetComponent<SteamVR_TrackedObject>();
        UDPScript = network.GetComponent<UDP>();
    }
    // Use this for initialization
    void Start () {
        lightsaber = Instantiate(lightsaberPrefab);

        //if (SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Leftmost) == 1)
        //{
        //leftIndex = SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Leftmost);
        //leftDevice = SteamVR_Controller.Input(leftIndex);
        //}

        //if (SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Rightmost) == 2)
        //{
        //rightIndex = SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Rightmost);
        //rightDevice = SteamVR_Controller.Input(rightIndex);
        //}
    }

    // Update is called once per frame
    void Update () {
        lightsaber.transform.position = trackedObj.transform.position;
        lightsaber.transform.rotation = trackedObj.transform.rotation * Quaternion.Euler(90, 0, 0);

        //if (SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Leftmost) == Controller.index)
        //{
        //    rightController.transform.rotation = leftDevice.transform.rot * Quaternion.Euler(180, 0, 90);
        //    rightController.transform.position = leftDevice.transform.pos;// + new Vector3(0.01f, 0.06f, 0.11f);
        //    //rightController.transform.position = leftDevice.transform.pos + new Vector3(posX, posY, posZ);
        //    //if (SteamVR_Controller.Input(SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Leftmost)).GetHairTriggerDown())
        //    //{
        //    //    Debug.Log("LEFT");
        //    //}
        //}

        //if (SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Rightmost) == Controller.index)
        //{
        //    leftController.transform.rotation = rightDevice.transform.rot * Quaternion.Euler(0, 0, 90);
        //    leftController.transform.position = rightDevice.transform.pos;// + new Vector3(-0.01f, 0.06f, 0.11f);
        //    //leftController.transform.position = rightDevice.transform.pos + new Vector3(posX, posY, posZ);
        //    //if (SteamVR_Controller.Input(SteamVR_Controller.GetDeviceIndex(SteamVR_Controller.DeviceRelation.Rightmost)).GetHairTriggerDown())
        //    //{
        //    //    Debug.Log("RIGHT");
        //    //}
        //}

        if (Controller.GetHairTriggerDown())
        {
            //Debug.Log("Trigger");
            //UDPScript.sendString("Trigger");
            //UDPScript.sendString(Random.Range(1, 4).ToString());
            //print(transform.position);
        }


    }


}
