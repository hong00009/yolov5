## 목차

1. git-clone

2. 폴더 생성 확인 

3. 브랜치 생성  git branch "브랜치이름"

4. 브랜치 전환 git switch "branch이름" (master > branch이름으로 변경됨)

5. local에서 remote로 파일 업로드 (git add, commit, push)

6. Pull Request
 
---
### 1. git-clone

- 깃허브 repository에서 Code 초록버튼 클릭

- url 복사

- vscode 터미널 열기 


적절한 위치를 경로로 하고, 터미널에

```sh
git clone "url"
```

※ git-clone시 자동으로 폴더가 생성되므로, 따로 폴더는 만들지 않아도 됩니다.



- 로컬에 팀원 분의 repository를 불러오는 작업


### 2. 폴더 생성 확인 

- 작업물까지 같이 들어온 것을 확인 가능하다.

- vscode 해당 폴더로 열어주기
 

### 3. 브랜치 생성 

팀원들이 각각, 파일을 올리는 공간을 생성해주는 것이다.

main 1곳에 다 올려버리면, 파일이 꼬일 수 있으므로 분리합니다.
```sh
git branch "branch이름"
```
(팀원의 이름으로 설정)

 
*초기 설정하시는 분은 main branch를 먼저 세팅해주셔야 한다.

(처음 repositroy 만들때 READ.md 파일 넣으면,자동으로 main branch 생성)

github repository에서 4개의 branch가 생성된 걸 확인 가능합니다.
 
### 4. 브랜치 전환

```sh
git switch "branch이름"
```
ex) git switch main
 

### 5. local에서 remote로 파일 업로드

```sh
git add .
```

커밋되기 전 상태 (staging으로 올린다)

→ 모든 파일을 staging 해준다.

```sh
 git commit -sm "Update : test"
```

s 옵션은 서명을 포함하는 옵션

-아직 local 환경에만 있는 상태

git commit 다음의 메시지는 convention (팀원들끼리 규칙을 정해서, commit message를 정한다.)


repository 연결하기

- repository를 만든 팀원에게 invite메일 보내달라고 요청하기

github 협업시, 아무나 repository에 파일을 올리면 안되므로, 권한 요청을 해야합니다

(fork 떠서, clone하는 방법은 상관없다고 합니다)

```sh
git push origin "branch이름"
```

- git 원격에 파일을 올리는 작업

-origin: 원격 origin과 연결 

branch 이름: 아까 설정한 곳으로 push할 것이다.


### 6. Pull Request

※ 터미널에서 push 후, github repository 페이지로 돌아와서 진행

-push가 됐다면, Pull Request를 날려야한다. (code-review를 하기 위함)

 merge하기 전에 confirm받는 공간 

※ git pull origin main

이것은 pull과 동시에 merge를 해주는 명령어다.

그래서 github 협업은 처음이니 꼬일까봐 merge를 하지 않는 pull request를 사용

 
해당 repository로 가서, 맨 오른쪽에 New PullRequest 클릭!

"branch → main으로 merge하기 전에 code-review 해주세요!!"

→ merge가 되지 않고, 일단 Pull request에 올라간다.

Pull request가 생성되면 다음과 같은 기능이 가능하다.

1. comment 달기

2. Merge 하기 

→ merge는 웬만하면 한 사람이 맡는다.

꼬이는 걸 관리하고, merge를 진행

---
### stash 기능

이미 작업하고 있던 중에 갑자기 원격저장소 master 기준 수정해야할 일이 생길때 임시저장 

1. 하던일 우선 저장

```git add .```

2. 간단한 메모와 함께 임시저장소로 이동시킴
   
```git stash save "남길말"```

4. 마스터 땡겨옴
   
```git pull origin master```

6. 마스터 수정하고 똑같이 깃 커밋 푸시, 완료 후
   
```git stash list```

8. 리스트에 있는 stash@{숫자} 중 본인이 임시저장한거 불러오기. 보통 0이 최신저장
   
```git stash pop stash@{0}```

10. 혹시 충돌 있다며 병합편집기 열리면 적절히 병합 선택
11. 수정하고 똑같이 깃 커밋 푸시, 마무리
