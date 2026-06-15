/**
 * CDK Exercise 04 — The "app.ts" Wiring Pattern
 * ================================================
 *
 * CONCEPTS:
 *   - cdk.App                → the root. ONE per CDK "app"; contains many Stacks.
 *   - cdk.Environment        → { account, region }. CDK reads CDK_DEFAULT_ACCOUNT /
 *                               CDK_DEFAULT_REGION (set by `cdk` CLI from your AWS
 *                               profile) — fall back to a literal region for local dev.
 *   - Deployment ORDER       → stacks are listed in dependency order in app.ts.
 *     CDK also infers a deploy ORDER automatically from cross-stack references
 *     (`cdk deploy --all` topologically sorts them), but listing them in order
 *     in app.ts makes the architecture readable top-to-bottom.
 *   - Cross-stack references → pass a stack's `readonly` properties (resource
 *     OBJECTS or plain strings derived from them) as props to the next stack's
 *     constructor. CDK auto-creates CloudFormation Fn::ImportValue / Outputs —
 *     you never write ARNs by hand.
 *   - app.synth()            → MUST be the last line. Renders every stack to
 *     CloudFormation templates under cdk.out/.
 *
 * REAL-WORLD REFERENCE:
 *   This mirrors bin/app.ts in aws-etl-pipeline-cdk, which wires together
 *   StorageStack → GlueStack → SageMakerStack → OrchestrationStack → MonitoringStack
 *   → AgentCoreStack (6 stacks, each depending on outputs from earlier ones).
 *
 * GIVEN (already complete — these are simplified stand-ins for
 * Exercise 01's StorageStack and Exercise 02's GlueStack so this file is
 * self-contained. Read them, but the TASK below is the wiring, not these.)
 *
 * RUN:
 *   cd typescript/cdk && npm install   (if you haven't already)
 *   npx tsx exercises/04_app_wiring.ts
 */

import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as s3 from 'aws-cdk-lib/aws-s3';
import * as glue from 'aws-cdk-lib/aws-glue';
import { Template } from 'aws-cdk-lib/assertions';

// ── GIVEN: Stack 1 — Storage ────────────────────────────────────────────────
class StorageStack extends cdk.Stack {
  readonly processedBucket: s3.Bucket;

  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    this.processedBucket = new s3.Bucket(this, 'ProcessedBucket', {
      removalPolicy:     cdk.RemovalPolicy.DESTROY,
      autoDeleteObjects: true,
    });
  }
}

// ── GIVEN: Stack 2 — Glue (depends on Stack 1's bucket) ─────────────────────
interface GlueStackProps extends cdk.StackProps {
  processedBucket: s3.Bucket;
}

class GlueStack extends cdk.Stack {
  readonly jobName: string;

  constructor(scope: Construct, id: string, props: GlueStackProps) {
    super(scope, id, props);

    this.jobName = 'practice-transform-job';

    const job = new glue.CfnJob(this, 'TransformJob', {
      name: this.jobName,
      role: 'arn:aws:iam::123456789012:role/placeholder', // a real stack would build this role
      command: {
        name:           'glueetl',
        pythonVersion:  '3',
        scriptLocation: `s3://${props.processedBucket.bucketName}/jobs/transform.py`,
      },
      glueVersion: '4.0',
    });
    void job;
  }
}

// ── GIVEN: Stack 3 — Orchestration (depends on Stack 2's job name) ─────────
interface OrchestrationStackProps extends cdk.StackProps {
  glueJobName: string;
}

class OrchestrationStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: OrchestrationStackProps) {
    super(scope, id, props);
    // (kept minimal — Exercise 03 is where you build the real state machine)
    new cdk.CfnOutput(this, 'WiredGlueJobName', { value: props.glueJobName });
  }
}

// ---- TASK: write the app.ts wiring ----
//
// 1. const app = new cdk.App();
//
// 2. Build an `env: cdk.Environment` object:
//      account: process.env.CDK_DEFAULT_ACCOUNT
//      region:  process.env.CDK_DEFAULT_REGION ?? 'us-east-1'
//
// 3. Instantiate StorageStack first (no dependencies):
//      const storage = new StorageStack(app, 'PracticeStorage', { env });
//
// 4. Instantiate GlueStack, passing storage's bucket as a prop:
//      const glueStack = new GlueStack(app, 'PracticeGlue', {
//        env,
//        processedBucket: storage.processedBucket,
//      });
//
// 5. Instantiate OrchestrationStack, passing glueStack.jobName (a plain string —
//    no cross-stack CloudFormation reference needed for a plain string output):
//      new OrchestrationStack(app, 'PracticeOrchestration', {
//        env,
//        glueJobName: glueStack.jobName,
//      });
//
// 6. app.synth();   ← MUST be last

// YOUR CODE HERE

// ---- TESTS ---- (uncomment after implementing)
//
// app.synth() must not throw. Then check that GlueStack's template contains a
// CROSS-STACK REFERENCE to StorageStack's bucket — CDK represents this as
// "Fn::ImportValue" in the synthesized template (CDK auto-creates an Output
// in StorageStack and an ImportValue in GlueStack).

/*
app.synth();

const glueTemplate = Template.fromStack(glueStack);
const glueJson = JSON.stringify(glueTemplate.toJSON());
console.assert(glueJson.includes('Fn::ImportValue'), 'GlueStack should import a value from StorageStack');

// OrchestrationStack got the job name as a plain string (no import needed)
const orchTemplate = Template.fromStack(app.node.findChild('PracticeOrchestration') as cdk.Stack);
orchTemplate.hasOutput('WiredGlueJobName', { Value: 'practice-transform-job' });

console.log('✓ 04_app_wiring — all tests passed');
*/
