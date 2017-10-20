using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BaxterController : MonoBehaviour {

    private SteamVR_TrackedObject trackedObj;

    [SerializeField]
    private UDPEditMode UDPScript;
    private UDPSend udpSend;
    private UDPReceive udpReceive;
    public GameObject network;

    public GameObject baxterTracker;
    public GameObject hmd;

    //private Animator anim;
    //private AnimatorStateInfo currentBaseState;

    Vector3 prevLoc;

    //public string cancelId;
    int nextUpdate = 1;
    [Header("Baxter Arm Position and Rotation")]
    [SerializeField] private List<string> baxterRecordings;
    public string baxterRecordFileName;

    [SerializeField] private List<Vector3> leftArmPositions;
    [Tooltip("Degrees")]
    [SerializeField] private List<Vector3> leftArmRotations;
    [SerializeField] private List<Vector3> rightArmPositions;
    [Tooltip("Degrees")]
    [SerializeField] private List<Vector3> rightArmRotations;

    public List<BaxterCommands> baxterCmdList;

    public struct BaxterCommands
    {
        public string armName;
        public Vector3 armPos;
        public Quaternion armRot;

        public BaxterCommands(string ArmName, Vector3 ArmPos, Quaternion ArmRot)
        {
            armName = ArmName;
            armPos = ArmPos;
            armRot = ArmRot;
        }
    }

    public Quaternion DegreesToQuaternion(Vector3 vec3)
    {
        return Quaternion.Euler(vec3);
    }

    public void StoreBaxterCommandList()
    {
        if (leftArmPositions.Count != leftArmRotations.Count)
        {
            Debug.LogError("Number of left arm positions not equal to number of left arm rotations." +
                "Each left arm position should have a related left arm rotation and vice versa.");
            return;
        }

        if (rightArmPositions.Count != rightArmRotations.Count)
        {
            Debug.LogError("Number of rightArmPositions not equal to number of rightArmRotations. " +
                "Each left arm position should have a related left arm rotation and vice versa.");
            return;
        }

        for (int i = 0; i < leftArmPositions.Count; i++)
        {
            baxterCmdList.Add(new BaxterCommands("left", leftArmPositions[i], DegreesToQuaternion(leftArmRotations[i])));
        }

        for (int i = 0; i < rightArmPositions.Count; i++)
        {
            baxterCmdList.Add(new BaxterCommands("right", rightArmPositions[i], DegreesToQuaternion(rightArmRotations[i])));
        }

    }

    private void RecordingListCheck(string fileName)
    {
        foreach (string str in baxterRecordings)
        {
            if (str == fileName)
            {
                Debug.LogWarning(fileName + " baxter recording is overwritten.");
            }
            else
            {
                baxterRecordings.Add(fileName);
            }
        }
    }

    public void RecordMovement()
    {
        Debug.Log("Record");
        if (baxterRecordFileName != "")
        {
            UDPScript.sendString("Record " + baxterRecordFileName);
            RecordingListCheck(baxterRecordFileName);
        }
        else
        {
            UDPScript.sendString("Record baxter_recording");
            RecordingListCheck("baxter_recording");
        }
        
    }

    public void StopRecording()
    {
        Debug.Log("Stop Recording");
        UDPScript.sendString("Stop");
    }

    public void PlaybackMovement()
    {
        Debug.Log("Playback");
        UDPScript.sendString("Play " + baxterRecordFileName);
    }

    public void SendBaxterMessage(int num)
    {
        udpSend.sendString(ArmMoveCmd("left", new Vector3(posX, posY, posZ), DegreesToQuaternion(new Vector3(rotX, rotY, rotZ))));
        //udpSend.sendString(ArmMoveCmd(baxterCmdList[num].armName, baxterCmdList[num].armPos, baxterCmdList[num].armRot));
        //udpSend.sendString(cmd.ArmMoveCmd(baxterCmdList[num].armName, baxterCmdList[num].armPos.x, baxterCmdList[num].armPos.y, baxterCmdList[num].armPos.z, baxterCmdList[num].armRot.x, baxterCmdList[num].armRot.y, baxterCmdList[num].armRot.z, baxterCmdList[num].armRot.w));
    }

    private void Awake()
    {
        UDPScript = network.GetComponent<UDPEditMode>();
        udpSend = network.GetComponent<UDPSend>();
        udpReceive = network.GetComponent<UDPReceive>();
        baxterCmdList = new List<BaxterCommands>();
    }
        
    private void Start()
    {
        prevLoc = Vector3.zero;

        StoreBaxterCommandList();
    }

    [SerializeField] float posX, posY, posZ, rotX, rotY, rotZ = 0;

    void BaxterLookAt()
    {
        float theta = Mathf.Atan((hmd.transform.position.x - baxterTracker.transform.position.x) / (hmd.transform.position.z - baxterTracker.transform.position.z));
        //print("enemy_face_angle(" + theta + ")");
        udpSend.sendString("enemy_face_angle(" + theta + ")");
    }

    // Update is called once per frame
    void Update () {

        BaxterLookAt();

        // Timer
        if (Time.time >= nextUpdate)
        {
            nextUpdate = Mathf.FloorToInt(Time.time) + 5;
            //print(cmd.ArmMoveCmd("left", new Vector3(1, 1, 1), new Quaternion(1, 1, 1, 1)));
            //udpSend.sendString(Random.Range(1, 4).ToString());
            //udpSend.sendString(cmd.ArmMoveCmd("left", new Vector3(1, 1, 1), new Quaternion(1, 1, 1, 1)));
            //print("Sent");
        }

        if (Input.GetKey(KeyCode.Q))
        {
            posX += 0.01f;
        }

        if (Input.GetKey(KeyCode.A))
        {
            posX -= 0.01f;
        }

        if (Input.GetKey(KeyCode.W))
        {
            posY += 0.01f;
        }

        if (Input.GetKey(KeyCode.S))
        {
            posY -= 0.01f;
        }

        if (Input.GetKey(KeyCode.E))
        {
            posZ += 0.01f;
        }

        if (Input.GetKey(KeyCode.D))
        {
            posZ -= 0.01f;
        }

        if (Input.GetKey(KeyCode.R))
        {
            rotX += 0.01f;
        }

        if (Input.GetKey(KeyCode.F))
        {
            rotX -= 0.01f;
        }

        if (Input.GetKey(KeyCode.T))
        {
            rotY += 0.01f;
        }

        if (Input.GetKey(KeyCode.G))
        {
            rotY -= 0.01f;
        }

        if (Input.GetKey(KeyCode.Y))
        {
            rotZ += 0.01f;
        }

        if (Input.GetKey(KeyCode.H))
        {
            rotZ -= 0.01f;
        }

        if (Input.GetKeyDown(KeyCode.Space))
        {
            //UDPScript.sendString("clash");
            //SendBaxterMessage(0);
            //udpSend.sendString(ArmMoveCmd("left", new Vector3(posX, posY, posZ), DegreesToQuaternion(new Vector3(rotX, rotY, rotZ))));
            //UDPScript.sendString(Random.Range(1, 4).ToString());
            //udpSend.sendString(cmd.ArmMoveCmd("left", 1.5f, 1.5f, 1.5f, 1.5f, 1.5f, 1.5f, 1.5f));
            //udpSend.sendString(cmd.ArmMoveCmd("left", new Vector3(1, 0, 1), new Quaternion(1, 0, 0, 1)));
        }
        //Vector3 vDir = (transform.position - prevLoc) / Time.deltaTime;
        //if (vDir.x > 0.5f)
        //{
        //    Debug.Log("Right");
        //}
        //else if (vDir.x < -0.5f)
        //{
        //    Debug.Log("Left");
        //}

        //if (vDir.z > 0.5f)
        //{
        //    Debug.Log("Forward");

        //}
        //else if (vDir.z < -0.5f)
        //{
        //    Debug.Log("Back");
        //}

        //prevLoc = transform.position;

        //cancelId = udpReceive.lastReceivedUDPPacket;
        //print("hello");
        //print(cmd.ArmMoveCmd("left", new Vector3(1, 1, 1), new Quaternion(1, 1, 1, 1)));
    }

    public string ArmMoveCmd(string arm, Vector3 pos, Quaternion rot)
    {
        //string cmd = string.Format("move_arm|" + arm + "|" + pos.ToString() + "|" + rot.ToString());
        string cmd = string.Format("move_arm|" + arm + "|(" + pos.x.ToString() + "," + pos.y.ToString() + "," + pos.z.ToString() + ")|(" + rot.x.ToString() + "," + rot.y.ToString() + "," + rot.z.ToString() + "," + rot.w.ToString() + ")");
        return cmd;
    }
}
